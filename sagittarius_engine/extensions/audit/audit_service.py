from datetime import datetime, timezone
from typing import Any, Dict, List
import platform
import json
import threading
import socketserver
import http.server
import logging
import platform
from sagittarius_engine.interfaces import IEngineContext
from sagittarius_engine.extensions.health_check_query import HealthCheckQuery, HealthCheckDTO


class AuditService:
    """
    @brief Collects telemetry and metrics from the EngineContext for the Audit Dashboard.
    """

    def __init__(self, context: IEngineContext, port: int = 9999) -> None:
        self.context = context
        self.port = port
        self.start_time = datetime.now(timezone.utc)
        self._server_thread = None
        self._httpd = None
        self._logger = logging.getLogger("AuditService")

    def start_server(self) -> None:
        """Starts the background telemetry HTTP server."""
        if self._server_thread and self._server_thread.is_alive():
            return

        class TelemetryHandler(http.server.SimpleHTTPRequestHandler):
            service_ref = self  # Reference to AuditService

            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                payload = {
                    "uptime": self.service_ref.get_uptime_seconds(),
                    "environment": self.service_ref.get_environment_info(),
                    "health": self.service_ref.get_system_health(),
                    "tasks": self.service_ref.get_active_tasks(),
                    "extensions": self.service_ref.get_loaded_extensions(),
                    "services": self.service_ref.get_running_hosted_services(),
                    "config_bus": self.service_ref.get_config_and_event_bus_info(),
                }
                self.wfile.write(json.dumps(payload).encode("utf-8"))

            def log_message(self, format, *args):
                # Suppress default HTTP server logging to avoid terminal clutter
                pass

        try:
            # Allow port reuse
            socketserver.TCPServer.allow_reuse_address = True
            self._httpd = socketserver.TCPServer(("", self.port), TelemetryHandler)
            self._server_thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
            self._server_thread.start()
            self._logger.info(f"Audit Telemetry Server listening on http://localhost:{self.port}")
        except Exception as e:
            self._logger.error(f"Failed to start Audit Telemetry Server: {e}")

    def stop_server(self) -> None:
        """Stops the background HTTP server."""
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None
        if self._server_thread:
            self._server_thread.join(timeout=1.0)
            self._server_thread = None

    def get_uptime_seconds(self) -> float:
        """
        @brief Returns engine uptime in seconds.
        """
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

    def get_system_health(self) -> dict[str, Any]:
        """
        @brief Dispatches HealthCheckQuery to get system health.
        """
        # Since IEngineContext doesn't expose dispatcher directly, we cast/duck-type
        try:
            app = getattr(self.context, "app", None)
            if app and hasattr(app, "query"):
                return app.query(HealthCheckQuery, HealthCheckDTO())
            
            # Fallback if dispatcher is accessible directly
            dispatcher = getattr(self.context, "dispatcher", None)
            if dispatcher:
                return dispatcher.query(HealthCheckQuery, HealthCheckDTO())
                
        except Exception as e:
            return {"status": "error", "message": str(e), "components": {}}

        return {"status": "unknown"}

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """
        @brief Returns a list of active background tasks.
        """
        tasks_data = []
        try:
            # ITaskManager stores tasks in a .tasks dictionary
            tasks_dict = getattr(self.context.tasks, "tasks", {})
            for task_id, task in tasks_dict.items():
                runtime = "N/A"
                if hasattr(task, "start_time") and task.start_time:
                    end = task.end_time or datetime.now(timezone.utc)
                    runtime = f"{(end - task.start_time).total_seconds():.1f}s"
                
                tasks_data.append({
                    "id": task_id[:8],
                    "name": getattr(task, "name", "Unknown"),
                    "status": getattr(task, "status", "Unknown"),
                    "runtime": runtime
                })
        except Exception:
            pass
        return tasks_data

    def get_loaded_extensions(self) -> List[Dict[str, Any]]:
        """
        @brief Returns a list of loaded extensions.
        """
        extensions_data = []
        try:
            ext_manager = getattr(self.context, "extension_manager", None)
            if ext_manager:
                for ext in ext_manager.registered_extensions:
                    desc = getattr(ext, "descriptor", None)
                    if desc:
                        extensions_data.append({
                            "name": desc.name,
                            "version": desc.version,
                            "enabled": desc.enabled
                        })
                    else:
                        extensions_data.append({
                            "name": ext.__class__.__name__,
                            "version": "unknown",
                            "enabled": True
                        })
        except Exception:
            pass
        return extensions_data

    def get_running_hosted_services(self) -> List[str]:
        """
        @brief Returns a list of running hosted services.
        """
        services_data = []
        try:
            hs_manager = getattr(self.context, "hosted_services", None)
            if hs_manager:
                for srv in hs_manager.started_services:
                    services_data.append(srv.__class__.__name__)
        except Exception:
            pass
        return services_data

    def get_environment_info(self) -> Dict[str, str]:
        """
        @brief Returns basic OS and Python environment info.
        """
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version()
        }

    def get_config_and_event_bus_info(self) -> Dict[str, Any]:
        """
        @brief Returns high-level config keys and event bus subscriptions.
        """
        info = {"event_bus_handlers": {}, "config_keys": []}
        try:
            eb = getattr(self.context, "event_bus", None)
            if eb and hasattr(eb, "_handlers"):
                for event_name, handlers in eb._handlers.items():
                    info["event_bus_handlers"][event_name] = len(handlers)
            
            from sagittarius_engine.interfaces import IConfig
            config = self.context.container.resolve(IConfig)
            if config and hasattr(config, "_config"):
                info["config_keys"] = list(config._config.keys())
        except Exception:
            pass
        return info
