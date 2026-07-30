from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import platform
import json
import threading
import socketserver
import http.server
import logging
from sagittarius_engine.interfaces import IEngineContext
from collections import deque
from sagittarius_engine.extensions.health_check_query import (
    HealthCheckQuery,
    HealthCheckDTO,
)

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class AuditService:
    """
    @brief Collects telemetry and metrics from the EngineContext for the Audit Dashboard.
    """

    def __init__(self, context: IEngineContext, port: int = 9999) -> None:
        self.context: IEngineContext = context
        self.port: int = port
        self.start_time: datetime = datetime.now(timezone.utc)
        self._server_thread: Optional[threading.Thread] = None
        self._httpd: Optional[socketserver.TCPServer] = None
        self._logger: logging.Logger = logging.getLogger("AuditService")
        self.recent_events: deque = deque(maxlen=100)
        self._hook_event_bus()

    def _hook_event_bus(self) -> None:
        try:
            eb = getattr(self.context, "event_bus", None)
            if eb and hasattr(eb, "emit"):
                original_emit = eb.emit

                def emit_hook(event_name_or_obj: Any, data: Any = None) -> None:
                    # Record event
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    if isinstance(event_name_or_obj, str):
                        name = event_name_or_obj
                    elif hasattr(event_name_or_obj, "__class__"):
                        name = event_name_or_obj.__class__.__name__
                    else:
                        name = str(event_name_or_obj)

                    self.recent_events.append(f"[{timestamp}] {name}")

                    # Call original emit
                    original_emit(event_name_or_obj, data)

                eb.emit = emit_hook
        except Exception:
            pass  # nosec B110

    def start_server(self) -> None:
        """Starts the background telemetry HTTP server."""
        if self._server_thread and self._server_thread.is_alive():
            return

        class TelemetryHandler(http.server.SimpleHTTPRequestHandler):
            service_ref = self  # Reference to AuditService

            def do_GET(self):
                if self.path == "/config":
                    payload = {"config": self.service_ref.get_full_config()}
                elif self.path == "/events":
                    payload = {"events": list(self.service_ref.recent_events)}
                elif self.path == "/tasks":
                    payload = {"tasks": self.service_ref.get_all_tasks_details()}
                elif self.path == "/":
                    payload = {
                        "uptime": self.service_ref.get_uptime_seconds(),
                        "environment": self.service_ref.get_environment_info(),
                        "health": self.service_ref.get_system_health(),
                        "tasks": self.service_ref.get_active_tasks(),
                        "extensions": self.service_ref.get_loaded_extensions(),
                        "services": self.service_ref.get_running_hosted_services(),
                        "config_bus": self.service_ref.get_config_and_event_bus_info(),
                        "pipeline": self.service_ref.get_middleware_pipeline(),
                        "scheduler": self.service_ref.get_scheduler_jobs(),
                        "recent_events": list(self.service_ref.recent_events)[
                            -10:
                        ],  # Only show last 10 for summary
                    }
                else:
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(payload).encode("utf-8"))

            def log_message(self, format, *args):
                # Suppress default HTTP server logging to avoid terminal clutter
                pass

        try:
            # Allow port reuse
            socketserver.TCPServer.allow_reuse_address = True
            self._httpd = socketserver.TCPServer(("", self.port), TelemetryHandler)
            self._server_thread = threading.Thread(
                target=self._httpd.serve_forever, daemon=True
            )
            self._server_thread.start()
            self._logger.info(
                f"Audit Telemetry Server listening on http://localhost:{self.port}"
            )
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

                tasks_data.append(
                    {
                        "id": task_id[:8],
                        "name": getattr(task, "name", "Unknown"),
                        "status": task.status.value
                        if hasattr(task.status, "value")
                        else str(task.status),
                        "progress": getattr(task, "progress", 0.0),
                        "runtime": runtime,
                    }
                )
        except Exception:
            pass  # nosec B110
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
                        extensions_data.append(
                            {
                                "name": desc.name,
                                "version": desc.version,
                                "enabled": desc.enabled,
                            }
                        )
                    else:
                        extensions_data.append(
                            {
                                "name": ext.__class__.__name__,
                                "version": "unknown",
                                "enabled": True,
                            }
                        )
        except Exception:
            pass  # nosec B110
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
            pass  # nosec B110
        return services_data

    def get_environment_info(self) -> Dict[str, str]:
        """
        @brief Returns basic OS, Python environment info, and System Metrics.
        """
        env = {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "cpu_percent": "N/A",
            "ram_mb": "N/A",
        }

        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                env["cpu_percent"] = f"{process.cpu_percent(interval=None):.1f}%"
                env["ram_mb"] = f"{process.memory_info().rss / 1024 / 1024:.1f} MB"
            except Exception:
                pass  # nosec B110

        return env

    def get_config_and_event_bus_info(self) -> Dict[str, Any]:
        """
        @brief Returns high-level config keys and event bus subscriptions.
        """
        info: Dict[str, Any] = {"event_bus_handlers": {}, "config_keys": []}
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
            pass  # nosec B110
        return info

    def get_middleware_pipeline(self) -> List[str]:
        """Returns the list of loaded middlewares."""
        try:
            pipeline = getattr(getattr(self.context, "app", None), "pipeline", None)
            if pipeline and hasattr(pipeline, "middlewares"):
                return [m.__class__.__name__ for m in pipeline.middlewares]
        except Exception:
            pass  # nosec B110
        return []

    def get_scheduler_jobs(self) -> List[Dict[str, str]]:
        """Returns scheduled jobs and next run time."""
        jobs_data = []
        try:
            scheduler = getattr(self.context, "scheduler", None)
            if scheduler and hasattr(scheduler, "jobs"):
                for job in scheduler.jobs:
                    job_name = getattr(job.job_func, "__name__", "anonymous_job")
                    next_run = (
                        job.next_run.strftime("%H:%M:%S")
                        if hasattr(job, "next_run") and job.next_run
                        else "Unknown"
                    )
                    jobs_data.append(
                        {
                            "name": job_name,
                            "interval": f"{job.interval}s",
                            "next_run": next_run,
                        }
                    )
        except Exception:
            pass  # nosec B110
        return jobs_data

    def get_full_config(self) -> Dict[str, Any]:
        """Returns the full configuration dictionary."""
        config = getattr(self.context, "config", None)
        if not config:
            return {}
        if hasattr(config, "_cache"):
            return getattr(config, "_cache", {})
        if hasattr(config, "store"):
            return getattr(config, "store", {})
        if hasattr(config, "_store"):
            return getattr(config, "_store", {})
        return {"error": "Unable to extract config dictionary from implementation"}

    def get_all_tasks_details(self) -> List[Dict[str, Any]]:
        """Returns detailed information of all background tasks including errors."""
        tasks = []
        try:
            tm = getattr(self.context, "tasks", None)
            if tm and hasattr(tm, "tasks"):
                tasks_dict = getattr(tm, "tasks", {})
                if isinstance(tasks_dict, dict):
                    task_items = tasks_dict.values()
                else:
                    task_items = tasks_dict

                for t in task_items:
                    error_msg = None
                    if hasattr(t, "error") and t.error:
                        error_msg = str(t.error)
                    elif hasattr(t, "exception") and t.exception:
                        error_msg = str(t.exception)

                    runtime = "N/A"
                    if hasattr(t, "start_time") and t.start_time:
                        end = getattr(t, "end_time", None) or datetime.now(timezone.utc)
                        runtime = f"{(end - t.start_time).total_seconds():.1f}s"

                    tasks.append(
                        {
                            "id": getattr(t, "id", getattr(t, "task_id", "Unknown")),
                            "name": getattr(t, "name", "Unknown"),
                            "status": t.status.value
                            if hasattr(t, "status") and hasattr(t.status, "value")
                            else str(getattr(t, "status", "Unknown")),
                            "progress": getattr(t, "progress", 0.0),
                            "runtime": runtime,
                            "error": error_msg,
                        }
                    )
        except Exception:
            pass  # nosec B110
        return tasks
