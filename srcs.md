# PROJECT CONTEXT

**Roots:**
- `/home/hoanganh/Documents/Sagittarius_ForkBoy/sagittarius_engine`

**Pattern:** `*.py`
**Generated:** 2026-08-04 16:04:52

## Directory Tree: /home/hoanganh/Documents/Sagittarius_ForkBoy/sagittarius_engine

```
sagittarius_engine
├── __init__.py
├── adapters
│   ├── batch
│   │   ├── __init__.py
│   │   ├── batch_input_port.py
│   │   ├── batch_output_port.py
│   │   └── const.py
│   └── cli
│       ├── __init__.py
│       ├── cli_input_port.py
│       ├── cli_output_port.py
│       └── const.py
├── base
│   ├── __init__.py
│   ├── base_input_port.py
│   ├── base_module.py
│   └── base_output_port.py
├── domain
│   ├── __init__.py
│   ├── base_event.py
│   └── i_domain_event.py
├── exceptions.py
├── extensions
│   ├── __init__.py
│   ├── audit
│   │   ├── __init__.py
│   │   ├── audit_extension.py
│   │   ├── audit_service.py
│   │   ├── events.py
│   │   ├── infra
│   │   │   ├── __init__.py
│   │   │   └── websocket_broadcaster.py
│   │   └── ports.py
│   ├── cqrs
│   │   ├── __init__.py
│   │   └── interfaces
│   │       ├── commands.py
│   │       └── queries.py
│   ├── health
│   │   ├── __init__.py
│   │   ├── health_check_query.py
│   │   └── health_module.py
│   ├── logger
│   │   ├── __init__.py
│   │   └── logger_module.py
│   ├── persistence
│   │   ├── __init__.py
│   │   ├── database_module.py
│   │   ├── i_session.py
│   │   ├── repository.py
│   │   └── sqlalchemy_session_adapter.py
│   └── thread_manager
│       ├── __init__.py
│       └── thread_manager_module.py
├── infrastructure
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── config_source.py
│   │   ├── config_sources
│   │   │   ├── __init__.py
│   │   │   └── dotenv_source.py
│   │   ├── dict_config.py
│   │   ├── dict_source.py
│   │   ├── env_source.py
│   │   └── json_source.py
│   ├── container
│   │   ├── __init__.py
│   │   ├── scope_context.py
│   │   └── std_container.py
│   ├── event_bus
│   │   ├── __init__.py
│   │   ├── asyncio_event_bus.py
│   │   ├── ipc_broker.py
│   │   ├── ipc_queue_event_bus.py
│   │   ├── memory_event_bus.py
│   │   ├── resilient_event_bus.py
│   │   └── thread_pool_event_bus.py
│   ├── logging
│   │   ├── __init__.py
│   │   ├── log_metrics.py
│   │   ├── logger_config.py
│   │   ├── std_logger.py
│   │   └── tcp_log_viewer_handler.py
│   ├── persistence
│   │   └── __init__.py
│   ├── storage
│   │   ├── __init__.py
│   │   ├── azure_blob_storage.py
│   │   ├── local_file_storage.py
│   │   └── s3_file_storage.py
│   └── thread_manager.py
├── interfaces
│   ├── __init__.py
│   ├── i_async_event_bus.py
│   ├── i_config.py
│   ├── i_container.py
│   ├── i_dispatchable.py
│   ├── i_engine_context.py
│   ├── i_event_bus.py
│   ├── i_extension.py
│   ├── i_file_storage.py
│   ├── i_input_port.py
│   ├── i_logger.py
│   ├── i_metrics.py
│   ├── i_middleware.py
│   ├── i_module.py
│   ├── i_output_port.py
│   ├── i_task_manager.py
│   └── i_thread_manager.py
├── kernel
│   ├── __init__.py
│   ├── app_runner.py
│   ├── app.py
│   ├── bootstrap.py
│   ├── context.py
│   ├── dispatcher.py
│   ├── events.py
│   ├── extension_manager.py
│   ├── i_kernel_context.py
│   ├── lifecycle.py
│   ├── middleware_pipeline.py
│   ├── module_auto_discovery.py
│   └── module_loader.py
├── middleware
│   ├── __init__.py
│   ├── logging_middleware.py
│   ├── pydantic_validation_middleware.py
│   ├── timing_middleware.py
│   ├── transaction_middleware.py
│   └── validation_middleware.py
├── runtime
│   ├── __init__.py
│   ├── async_runtime
│   │   ├── __init__.py
│   │   └── async_runtime.py
│   ├── hosted
│   │   ├── __init__.py
│   │   ├── background_service.py
│   │   ├── events.py
│   │   ├── hosted_service_manager.py
│   │   └── hosted_service.py
│   ├── scheduler
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── scheduler.py
│   │   └── triggers.py
│   └── tasks
│       ├── __init__.py
│       ├── background_task.py
│       ├── cancellation_token.py
│       ├── events.py
│       └── task_manager.py
├── sdk
│   ├── __init__.py
│   ├── cli.py
│   ├── project_generator.py
│   ├── template_loader.py
│   ├── template_renderer.py
│   └── templates
│       ├── clean
│       │   ├── adapters
│       │   │   └── __init__.py
│       │   ├── application
│       │   │   └── __init__.py
│       │   ├── domain
│       │   │   └── __init__.py
│       │   ├── infrastructure
│       │   │   └── __init__.py
│       │   ├── main.py
│       │   └── modules
│       │       └── __init__.py
│       ├── ddd
│       │   ├── application
│       │   │   └── __init__.py
│       │   ├── domain
│       │   │   ├── model
│       │   │   │   └── __init__.py
│       │   │   └── services
│       │   │       └── __init__.py
│       │   ├── infrastructure
│       │   │   └── __init__.py
│       │   ├── interfaces
│       │   │   └── __init__.py
│       │   └── main.py
│       ├── minimal
│       │   └── main.py
│       └── mvc
│           ├── controllers
│           │   └── __init__.py
│           ├── main.py
│           ├── models
│           │   └── __init__.py
│           └── views
│               └── __init__.py
└── utils
    ├── __init__.py
    ├── null_logger.py
    └── path_utils.py
```

---

# FILE: __init__.py

```python
from sagittarius_engine.kernel.app import App
from sagittarius_engine.kernel.context import EngineContext
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor
from sagittarius_engine.extensions.cqrs import ICommand, IQuery
from sagittarius_engine.extensions.persistence import BaseRepository

__all__ = [
    "App",
    "EngineContext",
    "IExtension",
    "ExtensionDescriptor",
    "ICommand",
    "IQuery",
    "BaseRepository",
]
``````

# FILE: adapters/batch/__init__.py

```python
from .batch_input_port import BatchInputPort
from .batch_output_port import BatchOutputPort
from .const import FILE_TYPE_CSV, FILE_TYPE_JSON

__all__ = ["BatchInputPort", "BatchOutputPort", "FILE_TYPE_CSV", "FILE_TYPE_JSON"]
``````

# FILE: adapters/batch/batch_input_port.py

```python
import csv
import json
import os
from typing import Any, Iterator, Optional
from sagittarius_engine.kernel.app_runner import COMMAND_KEY, EXIT_COMMAND
from sagittarius_engine.base.base_input_port import BaseInputPort
from sagittarius_engine.adapters.batch.const import FILE_TYPE_CSV, FILE_TYPE_JSON
from sagittarius_engine.exceptions import PathTraversalError

class BatchInputPort(BaseInputPort):

def process(self, filepath: str) -> None:
        pass

    def __init__(
        self,
        file_path: str,
        file_type: str = FILE_TYPE_CSV,
        base_path: Optional[str] = None,
    ) -> None:
        super().__init__()

        if base_path is not None:
            base_path_real = os.path.realpath(base_path)
            full_path = (
                os.path.join(base_path, file_path)
                if not os.path.isabs(file_path)
                else file_path
            )
            full_path_real = os.path.realpath(full_path)

            if os.path.commonpath([base_path_real, full_path_real]) != base_path_real:
                raise PathTraversalError(f"Path traversal detected: {file_path}")
            self.file_path = full_path_real
        else:
            self.file_path = file_path

        self.file_type = file_type
        self._iterator: Optional[Iterator[dict[str, Any]]] = None
        self._initialized = False

    def _init_iterator(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        if not os.path.exists(self.file_path):
            if self.logger:
                self.logger.error(f"File not found: {self.file_path}")
            self._iterator = iter([])
            return
        try:
            if self.file_type == FILE_TYPE_CSV:
                with open(self.file_path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    self._iterator = iter(data)
            elif self.file_type == FILE_TYPE_JSON:
                with open(self.file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._iterator = iter(data)
                    else:
                        if self.logger:
                            self.logger.error(
                                "JSON file must contain an array of objects"
                            )
                        self._iterator = iter([])
            else:
                if self.logger:
                    self.logger.error(f"Unsupported file type: {self.file_type}")
                self._iterator = iter([])
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading file {self.file_path}: {e}")
            self._iterator = iter([])

    def receive(self) -> dict[str, Any]:
        
        self._init_iterator()
        try:
            if self._iterator is not None:
                row = next(self._iterator)
                return row
            else:
                return {COMMAND_KEY: EXIT_COMMAND}
        except StopIteration:
            return {COMMAND_KEY: EXIT_COMMAND}
``````

# FILE: adapters/batch/batch_output_port.py

```python
import json
import os
from typing import Any
from sagittarius_engine.base.base_output_port import BaseOutputPort
from sagittarius_engine.exceptions import PathTraversalError

class BatchOutputPort(BaseOutputPort):

def __init__(self, output_path: str, base_path: str = "") -> None:
        super().__init__()

        base_path_real = os.path.realpath(base_path)
        full_path = (
            os.path.join(base_path, output_path)
            if not os.path.isabs(output_path)
            else output_path
        )
        full_path_real = os.path.realpath(full_path)

        if os.path.commonpath([base_path_real, full_path_real]) != base_path_real:
            raise PathTraversalError(f"Path traversal detected: {output_path}")

        self.output_path = full_path_real
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def present(self, result: Any) -> None:
        
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                if isinstance(result, dict):
                    f.write(json.dumps(result) + "\n")
                else:
                    f.write(str(result) + "\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")

    def present_error(self, error: Exception) -> None:
        
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(f"ERROR: {error}\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing to output file: {e}")
``````

# FILE: adapters/batch/const.py

```python
FILE_TYPE_CSV = "csv"
FILE_TYPE_JSON = "json"
EXIT_COMMAND = "exit"
``````

# FILE: adapters/cli/__init__.py

```python
from .cli_input_port import CLIInputPort
from .cli_output_port import CLIOutputPort
from .const import COMMAND_KEY

__all__ = ["CLIInputPort", "CLIOutputPort", "COMMAND_KEY"]
``````

# FILE: adapters/cli/cli_input_port.py

```python
import argparse
import sys
from typing import Any
from sagittarius_engine.base.base_input_port import BaseInputPort
from sagittarius_engine.adapters.cli.const import COMMAND_KEY

class CLIInputPort(BaseInputPort):

def receive(self) -> dict[str, Any]:
        
        parser = argparse.ArgumentParser(description="CLI Input Port")
        parser.add_argument(COMMAND_KEY, type=str, help="The command to execute")
        args, unknown = parser.parse_known_args()
        result = {COMMAND_KEY: getattr(args, COMMAND_KEY)}
        i = 0
        while i < len(unknown):
            arg = unknown[i]
            if arg.startswith("--"):
                key = arg[2:]
                value = None
                if i + 1 < len(unknown) and (not unknown[i + 1].startswith("--")):
                    value = unknown[i + 1]
                    i += 1
                result[key] = value
            else:
                sys.exit(f"error: unrecognized arguments: {arg}")
            i += 1
        return result
``````

# FILE: adapters/cli/cli_output_port.py

```python
import sys
from pprint import pprint
from typing import Any
from sagittarius_engine.base.base_output_port import BaseOutputPort

class CLIOutputPort(BaseOutputPort):

def present(self, result: Any) -> None:
        
        if result is not None:
            pprint(result)

    def present_error(self, error: Exception) -> None:
        
        print(f"ERROR: {error}", file=sys.stderr)
``````

# FILE: adapters/cli/const.py

```python
COMMAND_KEY = "command"
EXIT_COMMAND = "exit"
``````

# FILE: base/__init__.py

```python
from .base_module import BaseModule
from .base_input_port import BaseInputPort
from .base_output_port import BaseOutputPort

__all__ = [
    "BaseModule",
    "BaseInputPort",
    "BaseOutputPort",
]
``````

# FILE: base/base_input_port.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces.i_input_port import IInputPort
from sagittarius_engine.interfaces.i_logger import ILogger

class BaseInputPort(IInputPort):

def __init__(self, logger: Optional[ILogger] = None) -> None:
        self.logger = logger

    def receive(self) -> dict[str, Any]:
        
        raise NotImplementedError("Subclasses must implement receive()")
``````

# FILE: base/base_module.py

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel import App

from sagittarius_engine.interfaces.i_module import IModule

class BaseModule(IModule):

def register(self, app: "App") -> None:
        pass

    def boot(self, app: "App") -> None:
        pass
``````

# FILE: base/base_output_port.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_output_port import IOutputPort

class BaseOutputPort(IOutputPort):

def __init__(self, logger: Optional[ILogger] = None) -> None:
        self.logger = logger

    def present(self, result: Any) -> None:
        
        if self.logger:
            self.logger.info(f"Result: {result}")
        else:
            print(result)

    def present_error(self, error: Exception) -> None:
        
        if self.logger:
            self.logger.error(f"Error: {error}")
        else:
            print(f"Error: {error}")
``````

# FILE: domain/__init__.py

```python
from .i_domain_event import IDomainEvent
from .base_event import BaseEvent

__all__ = [
    "IDomainEvent",
    "BaseEvent",
]
``````

# FILE: domain/base_event.py

```python
import uuid
from datetime import UTC, datetime

from sagittarius_engine.domain.i_domain_event import IDomainEvent

class BaseEvent(IDomainEvent):

def __init__(self) -> None:
        self._event_id: str = str(uuid.uuid4())
        self._occurred_on: datetime = datetime.now(UTC)

    @property
    def event_id(self) -> str:
        return self._event_id

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

    def to_dict(self) -> dict:
        
        data = self.__dict__.copy()
        if "_event_id" in data:
            data["event_id"] = data.pop("_event_id")
        if "_occurred_on" in data:
            data["occurred_on"] = data.pop("_occurred_on")

        data["occurred_on"] = self.occurred_on.isoformat()
        return data
``````

# FILE: domain/i_domain_event.py

```python
from abc import ABC, abstractmethod
from datetime import datetime

class IDomainEvent(ABC):

@property
    @abstractmethod
    def event_id(self) -> str:
        
        pass

    @property
    @abstractmethod
    def occurred_on(self) -> datetime:
        
        pass
``````

# FILE: exceptions.py

```python
class ModuleRegistrationError(Exception):

pass

class DependencyResolutionError(Exception):

pass

class PathTraversalError(ValueError):

pass

class ExtensionDependencyError(Exception):

pass

class ExtensionCircularDependencyError(ExtensionDependencyError):

pass
``````

# FILE: extensions/__init__.py

```python


from .cqrs import ICommand, IQuery

from .audit import AuditExtension, AuditService

from .persistence import (
    BaseRepository,
    ISession,
    SQLAlchemySessionAdapter,
    DatabaseExtension,
    SqlAlchemyExtension,
)

from .health.health_module import HealthExtension, HealthUpdatedEvent
from .health.health_check_query import HealthCheckQuery, HealthCheckDTO

from .logger.logger_module import LoggerExtension

from .thread_manager.thread_manager_module import ThreadManagerModule

__all__ = [

    "ICommand",
    "IQuery",

    "AuditExtension",
    "AuditService",

    "BaseRepository",
    "ISession",
    "SQLAlchemySessionAdapter",
    "DatabaseExtension",
    "SqlAlchemyExtension",

    "HealthExtension",
    "HealthCheckQuery",
    "HealthCheckDTO",
    "HealthUpdatedEvent",

    "LoggerExtension",

    "ThreadManagerModule",
]
``````

# FILE: extensions/audit/__init__.py

```python
from .audit_service import AuditService
from .audit_extension import AuditExtension

__all__ = ["AuditService", "AuditExtension"]
``````

# FILE: extensions/audit/audit_extension.py

```python
from sagittarius_engine.interfaces import IEngineContext, IExtension
from sagittarius_engine.extensions.audit.audit_service import AuditService

class AuditExtension(IExtension):

def __init__(self, enable_dashboard: bool = False) -> None:
        self.enable_dashboard = enable_dashboard
        self.dependencies = ["HealthExtension"]

    def register(self, context: IEngineContext) -> None:
        
        audit_service = AuditService(context)
        context.container.singleton(AuditService, audit_service)

    def boot(self, context: IEngineContext) -> None:
        
        if self.enable_dashboard:
            audit_service = context.container.resolve(AuditService)
            audit_service.start_server()

    def shutdown(self, context: IEngineContext) -> None:
        
        if self.enable_dashboard:
            audit_service = context.container.resolve(AuditService)
            audit_service.stop_server()
``````

# FILE: extensions/audit/audit_service.py

```python
from datetime import datetime, timezone
from typing import Any, Dict, List
import platform
import logging
from collections import deque
from sagittarius_engine.interfaces import IEngineContext
from sagittarius_engine.extensions.health.health_check_query import (
    HealthCheckQuery,
    HealthCheckDTO,
)
from .infra.websocket_broadcaster import WebsocketBroadcaster

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class AuditService:

def __init__(self, context: IEngineContext, port: int = 9999) -> None:
        self.context: IEngineContext = context
        self.port: int = port
        self.start_time: datetime = datetime.now(timezone.utc)
        self._logger: logging.Logger = logging.getLogger("AuditService")
        self.recent_events: deque = deque(maxlen=100)

self.broadcaster = WebsocketBroadcaster(port=self.port)
        self.broadcaster.on_new_client_callback = self._get_full_state

        self._subscribe_events()

    def _get_full_state(self) -> Dict[str, Any]:
        return {
            "uptime": self.get_uptime_seconds(),
            "environment": self.get_environment_info(),
            "health": self.get_system_health(),
            "tasks": self.get_active_tasks(),
            "extensions": self.get_loaded_extensions(),
            "services": self.get_running_hosted_services(),
            "config_bus": self.get_config_and_event_bus_info(),
            "pipeline": self.get_middleware_pipeline(),
            "scheduler": self.get_scheduler_jobs(),
            "recent_events": list(self.recent_events)[-10:],
        }

    def _subscribe_events(self) -> None:
        try:
            eb = getattr(self.context, "event_bus", None)
            if not eb or not hasattr(eb, "on"):
                return

            def on_state_changed(event: Any) -> None:

                event_name = event.__class__.__name__
                if isinstance(event, str):
                    event_name = event
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.recent_events.append(f"[{timestamp}] {event_name}")

state = self._get_full_state()
                self.broadcaster.broadcast("state_update", state)

            from sagittarius_engine.runtime.tasks.events import (
                TaskStarted,
                TaskCompleted,
                TaskFailed,
            )

eb.on(TaskStarted, on_state_changed)
            eb.on(TaskCompleted, on_state_changed)
            eb.on(TaskFailed, on_state_changed)

eb.on("ExtensionLoaded", on_state_changed)
            eb.on("SystemStateChangedEvent", on_state_changed)

eb.on("student.added", on_state_changed)
            eb.on("student.updated", on_state_changed)
            eb.on("student.deleted", on_state_changed)
            eb.on("report.completed", on_state_changed)

        except Exception as e:
            self._logger.error(f"Failed to subscribe to events: {e}")

    def start_server(self) -> None:
        
        self.broadcaster.start()

    def stop_server(self) -> None:
        
        self.broadcaster.stop()

    def get_uptime_seconds(self) -> float:
        
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

    def get_system_health(self) -> dict[str, Any]:

try:
            app = getattr(self.context, "app", None)
            if app and hasattr(app, "dispatch"):
                return app.dispatch(HealthCheckQuery, HealthCheckDTO())

dispatcher = getattr(self.context, "dispatcher", None)
            if dispatcher:
                return dispatcher.dispatch(HealthCheckQuery, HealthCheckDTO())

        except Exception as e:
            return {"status": "error", "message": str(e), "components": {}}

        return {"status": "unknown"}

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        
        tasks_data = []
        try:

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
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return tasks_data

    def get_loaded_extensions(self) -> List[Dict[str, Any]]:
        
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
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return extensions_data

    def get_running_hosted_services(self) -> List[str]:
        
        services_data = []
        try:
            hs_manager = getattr(self.context, "hosted_services", None)
            if hs_manager:
                for srv in hs_manager.started_services:
                    services_data.append(srv.__class__.__name__)
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return services_data

    def get_environment_info(self) -> Dict[str, str]:
        
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
            except Exception as e:
                self._logger.error(f"Audit service error: {e}")

        return env

    def get_config_and_event_bus_info(self) -> Dict[str, Any]:
        
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
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return info

    def get_middleware_pipeline(self) -> List[str]:
        
        try:
            pipeline = getattr(getattr(self.context, "app", None), "pipeline", None)
            if pipeline and hasattr(pipeline, "middlewares"):
                return [m.__class__.__name__ for m in pipeline.middlewares]
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return []

    def get_scheduler_jobs(self) -> List[Dict[str, str]]:
        
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
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return jobs_data

    def get_full_config(self) -> Dict[str, Any]:
        
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
        except Exception as e:
            self._logger.error(f"Audit service error: {e}")
        return tasks
``````

# FILE: extensions/audit/events.py

```python
from sagittarius_engine.domain.base_event import BaseEvent
from typing import Dict, Any

class SystemStateChangedEvent(BaseEvent):

def __init__(self, state_snapshot: Dict[str, Any]):
        super().__init__()
        self.state_snapshot = state_snapshot

class TaskCompletedEvent(BaseEvent):

def __init__(self, task_id: str, status: str):
        super().__init__()
        self.task_id = task_id
        self.status = status
``````

# FILE: extensions/audit/infra/__init__.py

```python


from .websocket_broadcaster import WebsocketBroadcaster

__all__ = ["WebsocketBroadcaster"]
``````

# FILE: extensions/audit/infra/websocket_broadcaster.py

```python
import asyncio
import json
import logging
import threading
import sys
from typing import Any, Dict, Set, Callable, Optional
from ..ports import ITelemetryBroadcaster

try:
    try:
        from websockets.asyncio.server import serve
    except ImportError:
        from websockets.server import serve
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

class WebsocketBroadcaster(ITelemetryBroadcaster):
    def __init__(self, host: str = "0.0.0.0", port: int = 9999):
        self.host = host
        self.port = port
        self.clients: Set[Any] = set()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._logger = logging.getLogger("WebsocketBroadcaster")
        self._server = None

self.on_new_client_callback: Optional[Callable[[], Dict[str, Any]]] = None

    async def _handler(self, websocket, *args, **kwargs):
        self.clients.add(websocket)
        self._logger.info(f"New client connected: {websocket.remote_address}")

        if self.on_new_client_callback:
            try:
                initial_state = self.on_new_client_callback()
                payload = json.dumps({"event": "initial_state", "data": initial_state})
                await websocket.send(payload)
            except Exception as e:
                self._logger.error(f"Error sending initial state: {e}")

        try:

            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            self._logger.info(f"Client disconnected: {websocket.remote_address}")

    def _run_server(self):
        if not WEBSOCKETS_AVAILABLE:
            self._logger.error("websockets library not installed. Please install it.")
            return

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        self._stop_event = asyncio.Event()

        async def main():
            try:
                if "websockets.asyncio" in sys.modules:
                    async with serve(self._handler, self.host, self.port):
                        self._logger.info(
                            f"Websocket Broadcaster (asyncio) listening on ws://{self.host}:{self.port}"
                        )
                        await self._stop_event.wait()
                else:
                    start_server = serve(self._handler, self.host, self.port)
                    self._server = await start_server
                    self._logger.info(
                        f"Websocket Broadcaster (legacy) listening on ws://{self.host}:{self.port}"
                    )
                    await self._stop_event.wait()
            except asyncio.CancelledError:
                pass

        try:
            self._loop.run_until_complete(main())
        finally:
            self._loop.close()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._thread = threading.Thread(target=self._run_server, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._stop_event.set)

        if self._thread:
            self._thread.join(timeout=2.0)

    def broadcast(self, event_name: str, payload: Dict[str, Any]) -> None:
        if not self._loop or not self.clients:
            return

        message = json.dumps({"event": event_name, "data": payload})

        async def _broadcast():
            if not self.clients:
                return
            tasks = [
                asyncio.create_task(client.send(message)) for client in self.clients
            ]
            done, pending = await asyncio.wait(tasks, timeout=1.0)
            for t in pending:
                t.cancel()

        asyncio.run_coroutine_threadsafe(_broadcast(), self._loop)
``````

# FILE: extensions/audit/ports.py

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class ITelemetryBroadcaster(ABC):

@abstractmethod
    def start(self) -> None:
        
        ...

    @abstractmethod
    def stop(self) -> None:
        
        ...

    @abstractmethod
    def broadcast(self, event_name: str, payload: Dict[str, Any]) -> None:
        
        ...
``````

# FILE: extensions/cqrs/__init__.py

```python
from .interfaces.commands import ICommand
from .interfaces.queries import IQuery

__all__ = ["ICommand", "IQuery"]
``````

# FILE: extensions/cqrs/interfaces/commands.py

```python
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sagittarius_engine.interfaces.i_dispatchable import IDispatchable

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

class ICommand(Generic[TInput, TOutput], IDispatchable, ABC):

@abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        
        ...
``````

# FILE: extensions/cqrs/interfaces/queries.py

```python
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sagittarius_engine.interfaces.i_dispatchable import IDispatchable

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

class IQuery(Generic[TInput, TOutput], IDispatchable, ABC):

@abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        
        ...
``````

# FILE: extensions/health/__init__.py

```python

``````

# FILE: extensions/health/health_check_query.py

```python
from dataclasses import dataclass
from typing import Any
from sagittarius_engine.extensions.cqrs import IQuery
from sagittarius_engine.extensions.persistence import ISession
from sagittarius_engine.interfaces import IContainer, IEventBus

@dataclass
class HealthCheckDTO:

pass

class HealthCheckQuery(IQuery):

def __init__(self, container: IContainer, event_bus: IEventBus):
        self.container = container
        self.event_bus = event_bus

    def execute(self, input_dto: HealthCheckDTO | None = None) -> dict[str, Any]:
        
        status: dict[str, Any] = {
            "status": "healthy",
            "components": {
                "container": "ok",
                "event_bus": "ok",
                "database": "unknown",
            },
        }
        try:
            self.container.resolve(IContainer)
        except Exception:
            status["components"]["container"] = "error: container resolution failed"
            status["status"] = "unhealthy"
        try:
            if not hasattr(self.event_bus, "emit"):
                raise ValueError("event_bus has no emit method")
        except Exception:
            status["components"]["event_bus"] = "error: event bus check failed"
            status["status"] = "unhealthy"
        try:
            session: ISession = self.container.resolve(ISession)
            try:
                from sqlalchemy import text

                session.execute(text("SELECT 1"))
                status["components"]["database"] = "ok"
            except ImportError:
                status["components"]["database"] = "sqlalchemy not installed"
                status["status"] = "unhealthy"
            except Exception:
                status["components"]["database"] = "database connection failed"
                status["status"] = "unhealthy"
        except Exception:
            status["components"]["database"] = "not configured"
        return status
``````

# FILE: extensions/health/health_module.py

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.extensions.health.health_check_query import HealthCheckQuery
from sagittarius_engine.domain.base_event import BaseEvent
from typing import Any

class HealthUpdatedEvent(BaseEvent):
    event_name = "health.updated"

    def __init__(self, status: dict[str, Any]) -> None:
        super().__init__()
        self.status: dict[str, Any] = status

class HealthExtension(IExtension):

def register(self, context: "IEngineContext") -> None:
        
        context.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, context: "IEngineContext") -> None:
        
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        
        pass
``````

# FILE: extensions/logger/__init__.py

```python

``````

# FILE: extensions/logger/logger_module.py

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.interfaces import IConfig, ILogger

class LoggerExtension(IExtension):

def register(self, context: "IEngineContext") -> None:
        try:
            config: IConfig = context.container.resolve(IConfig)
        except Exception:
            config = None

        logger_instance = StdLogger(config)
        context.container.singleton(ILogger, logger_instance)

    def boot(self, context: "IEngineContext") -> None:
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        pass
``````

# FILE: extensions/persistence/__init__.py

```python
from .repository import BaseRepository
from .i_session import ISession
from .sqlalchemy_session_adapter import SQLAlchemySessionAdapter
from .database_module import DatabaseExtension, SqlAlchemyExtension

__all__ = [
    "BaseRepository",
    "ISession",
    "SQLAlchemySessionAdapter",
    "DatabaseExtension",
    "SqlAlchemyExtension",
]
``````

# FILE: extensions/persistence/database_module.py

```python
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.interfaces import IConfig, ILogger
from sagittarius_engine.extensions.persistence.i_session import ISession
from sagittarius_engine.extensions.persistence.sqlalchemy_session_adapter import (
    SQLAlchemySessionAdapter,
)

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    SQLALCHEMY_INSTALLED = True
except ImportError:
    SQLALCHEMY_INSTALLED = False

class DatabaseExtension(IExtension):

def register(self, context: "IEngineContext") -> None:
        logger = self._get_logger(context)
        if not SQLALCHEMY_INSTALLED:
            if logger:
                logger.warning(
                    "DatabaseExtension: sqlalchemy is not installed. Database setup skipped."
                )
            return
        try:
            config: IConfig = context.container.resolve(IConfig)
            env = str(
                config.get("env")
                or config.get("app.env")
                or os.environ.get("ENV")
                or os.environ.get("APP_ENV")
                or "development"
            ).lower()
            db_url = config.get("database.url")
            if not db_url:
                if env == "production":
                    raise ValueError(
                        "Database configuration 'database.url' is missing in production environment."
                    )
                else:
                    db_url = "sqlite:///:memory:"
                    if logger:
                        logger.info(
                            "DatabaseExtension: 'database.url' not found. Using default in-memory SQLite."
                        )
        except Exception as e:
            if isinstance(e, ValueError) and "production environment" in str(e):
                raise
            env = str(
                os.environ.get("ENV") or os.environ.get("APP_ENV") or "development"
            ).lower()
            if env == "production":
                raise ValueError(
                    f"Failed to resolve database configuration in production: {e}"
                ) from e
            db_url = "sqlite:///:memory:"
            if logger:
                logger.info(
                    "DatabaseExtension: IConfig not found or failed to resolve. Using default in-memory SQLite."
                )
        try:
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)
            Session = scoped_session(session_factory)
            session_adapter = SQLAlchemySessionAdapter(Session)
            context.container.singleton(ISession, session_adapter)
            if logger:
                logger.info(
                    f"DatabaseExtension: SQLAlchemy engine created for {db_url} and ISession registered."
                )
        except Exception as e:
            if logger:
                logger.error(f"DatabaseExtension: Failed to initialize database - {e}")

    def boot(self, context: "IEngineContext") -> None:
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        pass

    def _get_logger(self, context: "IEngineContext") -> ILogger | None:
        try:
            return context.container.resolve(ILogger)
        except Exception:
            return None

SqlAlchemyExtension = DatabaseExtension
``````

# FILE: extensions/persistence/i_session.py

```python
from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")

class ISession(ABC):

@abstractmethod
    def commit(self) -> None:
        
        ...

    @abstractmethod
    def rollback(self) -> None:
        
        ...

    @abstractmethod
    def execute(self, statement: Any, params: Any = None) -> Any:
        
        ...

    @abstractmethod
    def query(self, *entities: Any) -> Any:
        
        ...

    @abstractmethod
    def add(self, entity: Any) -> None:
        
        ...

    @abstractmethod
    def get(self, entity_class: type[T], entity_id: Any) -> T | None:
        
        ...

    @abstractmethod
    def merge(self, entity: Any) -> Any:
        
        ...

    @abstractmethod
    def delete(self, entity: Any) -> None:
        
        ...

    def close(self) -> None:
        
        pass

    def __enter__(self) -> "ISession":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type is not None:
                self.rollback()
        finally:
            self.close()
``````

# FILE: extensions/persistence/repository.py

```python
from typing import Any, Generic, TypeVar
from sagittarius_engine.extensions.persistence.i_session import ISession

T = TypeVar("T")
TId = TypeVar("TId", bound=Any)

class BaseRepository(Generic[T, TId]):

def __init__(self, session: ISession, entity_class: type[T]) -> None:
        
        self.session = session
        self.entity_class = entity_class

    def add(self, entity: T) -> None:
        
        self.session.add(entity)

    def get_by_id(self, entity_id: TId) -> T | None:
        
        return self.session.get(self.entity_class, entity_id)

    def list_all(self) -> list[T]:
        
        return self.session.query(self.entity_class).all()

    def update(self, entity: T) -> None:
        
        self.session.merge(entity)

    def delete(self, entity: T) -> None:
        
        self.session.delete(entity)
``````

# FILE: extensions/persistence/sqlalchemy_session_adapter.py

```python
from typing import Any
from sagittarius_engine.extensions.persistence.i_session import ISession

class SQLAlchemySessionAdapter(ISession):

def __init__(self, session: Any):
        self.session = session

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def execute(self, statement: Any, params: Any = None) -> Any:
        return self.session.execute(statement, params)

    def query(self, *entities: Any) -> Any:
        return self.session.query(*entities)

    def add(self, entity: Any) -> None:
        self.session.add(entity)

    def get(self, entity_class: type, entity_id: Any) -> Any | None:
        return self.session.get(entity_class, entity_id)

    def merge(self, entity: Any) -> Any:
        return self.session.merge(entity)

    def delete(self, entity: Any) -> None:
        self.session.delete(entity)

    def close(self) -> None:
        if hasattr(self.session, "remove"):
            self.session.remove()
        elif hasattr(self.session, "close"):
            self.session.close()
``````

# FILE: extensions/thread_manager/__init__.py

```python

``````

# FILE: extensions/thread_manager/thread_manager_module.py

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext
    from sagittarius_engine.interfaces.i_config import IConfig

    from sagittarius_engine.kernel.app import App

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.thread_manager import ThreadManager
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.interfaces.i_thread_manager import (
    IThreadManager,
)
from sagittarius_engine.interfaces.i_module import IModule

class ThreadManagerExtension(IExtension):

def register(self, context: "IEngineContext") -> None:

        config: Any = context.container.resolve(IConfig)

        max_workers = 4
        if config:
            max_workers = config.get("thread_manager.max_workers", 4)

        try:
            max_workers = int(max_workers)
        except (ValueError, TypeError):
            max_workers = 4

        thread_manager = ThreadManager(max_workers=max_workers)
        context.container.singleton(IThreadManager, thread_manager)

    def boot(self, context: "IEngineContext") -> None:
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        pass

class ThreadManagerModule(IModule):
    def register(self, app: "App") -> None:
        pass
``````

# FILE: infrastructure/__init__.py

```python
from .event_bus import (
    MemoryEventBus,
    ThreadPoolEventBus,
    AsyncioEventBus,
    ResilientEventBus,
    IPCBroker,
    IPCQueueEventBus,
)
from .storage import (
    LocalFileStorage,
    S3FileStorage,
    AzureBlobStorage,
)
from .config import (
    ConfigManager,
    DictConfig,
)
from .config.config_sources import (
    DotenvSource,
)
from .container import (
    StdLibContainer,
)
from .logging import (
    StdLogger,
    LogMetrics,
)
from .thread_manager import ThreadManager

__all__ = [
    "MemoryEventBus",
    "ThreadPoolEventBus",
    "AsyncioEventBus",
    "ResilientEventBus",
    "IPCBroker",
    "IPCQueueEventBus",
    "LocalFileStorage",
    "S3FileStorage",
    "AzureBlobStorage",
    "ConfigManager",
    "DictConfig",
    "DotenvSource",
    "StdLibContainer",
    "StdLogger",
    "LogMetrics",
    "ThreadManager",
]
``````

# FILE: infrastructure/config/__init__.py

```python
from .config_manager import ConfigManager
from .dict_config import DictConfig
from .config_source import ConfigSource
from .dict_source import DictSource
from .env_source import EnvSource
from .json_source import JsonSource

__all__ = [
    "ConfigManager",
    "DictConfig",
    "ConfigSource",
    "DictSource",
    "EnvSource",
    "JsonSource",
]
``````

# FILE: infrastructure/config/config_manager.py

```python
from typing import Any
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class ConfigManager(IConfig):

def __init__(self) -> None:
        
        self._sources: list[ConfigSource] = []
        self._cache: dict[str, Any] = {}
        self._loaded = False

    def add_source(self, source: ConfigSource) -> None:
        
        self._sources.append(source)
        self._loaded = False

    def load_json(self, filepath: str) -> "ConfigManager":
        
        from sagittarius_engine.infrastructure.config.json_source import JsonSource

        self.add_source(JsonSource(filepath))
        return self

    def load_env(self, prefix: str = "") -> "ConfigManager":
        
        from sagittarius_engine.infrastructure.config.env_source import EnvSource

        self.add_source(EnvSource(prefix=prefix))
        return self

    def load_dict(self, data: dict[str, Any]) -> "ConfigManager":
        
        from sagittarius_engine.infrastructure.config.dict_source import DictSource

        self.add_source(DictSource(data))
        return self

    @classmethod
    def from_json(cls, filepath: str) -> "ConfigManager":
        
        return cls().load_json(filepath)

    def _load(self) -> None:
        
        if self._loaded:
            return
        self._cache = {}
        for source in self._sources:
            try:
                data = source.read()
                self._cache.update(data)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Config read error: {e}")
        self._loaded = True

    def get(self, key: str, default: Any = None, cast: type[Any] | None = None) -> Any:
        self._load()
        val = self._cache.get(key, default)
        if cast is not None and val is not None and not isinstance(val, cast):
            try:
                return cast(val)
            except (ValueError, TypeError):
                return val
        return val

    def set(self, key: str, value: Any) -> None:
        
        self._load()
        self._cache[key] = value
``````

# FILE: infrastructure/config/config_source.py

```python
from abc import ABC, abstractmethod
from typing import Any

class ConfigSource(ABC):

@abstractmethod
    def read(self) -> dict[str, Any]:
        
        ...
``````

# FILE: infrastructure/config/config_sources/__init__.py

```python
from .dotenv_source import DotenvSource

__all__ = ["DotenvSource"]
``````

# FILE: infrastructure/config/config_sources/dotenv_source.py

```python
import os
from typing import Any

from sagittarius_engine.infrastructure.config.config_source import ConfigSource

try:
    from dotenv import load_dotenv

    DOTENV_INSTALLED = True
except ImportError:
    DOTENV_INSTALLED = False

class DotenvSource(ConfigSource):

def __init__(self, filepath: str = ".env") -> None:
        
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        
        if not os.path.exists(self.filepath):
            return {}

        result = {}
        if DOTENV_INSTALLED:
            load_dotenv(dotenv_path=self.filepath)

from dotenv import dotenv_values

            return dotenv_values(dotenv_path=self.filepath)

        with open(self.filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip()

                    if (v.startswith('"') and v.endswith('"')) or (
                        v.startswith("'") and v.endswith("'")
                    ):
                        v = v[1:-1]
                    result[k] = v

                    os.environ[k] = v
        return result
``````

# FILE: infrastructure/config/dict_config.py

```python
from typing import Any

from sagittarius_engine.interfaces import IConfig

class DictConfig(IConfig):

def __init__(self, initial_data: dict[str, Any] | None = None) -> None:
        
        self._config: dict[str, Any] = initial_data if initial_data is not None else {}

    def get(self, key: str, default: Any = None, cast: type[Any] | None = None) -> Any:
        val = self._config.get(key, default)
        if cast is not None and val is not None and not isinstance(val, cast):
            try:
                return cast(val)
            except (ValueError, TypeError):
                return val
        return val

    def set(self, key: str, value: Any) -> None:
        
        self._config[key] = value
``````

# FILE: infrastructure/config/dict_source.py

```python
from typing import Any
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class DictSource(ConfigSource):

def __init__(self, data: dict[str, Any]) -> None:
        
        self.data = data

    def read(self) -> dict[str, Any]:
        
        return self.data
``````

# FILE: infrastructure/config/env_source.py

```python
import os
from typing import Any
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class EnvSource(ConfigSource):

def __init__(self, prefix: str = "") -> None:
        
        self.prefix = prefix

    def read(self) -> dict[str, Any]:
        
        result = {}
        for k, v in os.environ.items():
            if k.startswith(self.prefix):
                key = k[len(self.prefix) :]
                result[key] = v
        return result
``````

# FILE: infrastructure/config/json_source.py

```python
import os
import json
from typing import Any
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class JsonSource(ConfigSource):

def __init__(self, filepath: str) -> None:
        
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
``````

# FILE: infrastructure/container/__init__.py

```python
from .std_container import StdLibContainer

__all__ = [
    "StdLibContainer",
]
``````

# FILE: infrastructure/container/scope_context.py

```python
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

_current_scope: ContextVar[dict[type, Any] | None] = ContextVar(
    "_current_scope", default=None
)

class ScopeContext:

def __init__(self, scoped_registry: dict[type, type]) -> None:
        self._scoped_registry = scoped_registry
        self._token: Any = None

    def __enter__(self) -> "ScopeContext":
        self._token = _current_scope.set({})
        return self

    def __exit__(self, *args: object) -> None:
        _current_scope.reset(self._token)

    def resolve(self, abstract: type) -> Any | None:
        
        scope = _current_scope.get()
        if scope is None:
            return None

        concrete = self._scoped_registry.get(abstract)
        if concrete is None:
            return None

        if abstract not in scope:
            scope[abstract] = concrete()

        return scope[abstract]
``````

# FILE: infrastructure/container/std_container.py

```python
import inspect
import threading
from collections.abc import Callable
from typing import Any, TypeVar

from sagittarius_engine.exceptions import DependencyResolutionError
from sagittarius_engine.interfaces import IContainer
from sagittarius_engine.infrastructure.container.scope_context import ScopeContext

T = TypeVar("T")

class StdLibContainer(IContainer):

def __init__(self) -> None:
        self._lock = threading.RLock()
        self._bindings: dict[type, type] = {}
        self._instances: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}
        self._scoped_registry: dict[type, type] = {}
        self._scope_context: ScopeContext = ScopeContext(self._scoped_registry)

        self._resolution_cache: dict[type, dict[str, dict[str, Any]]] = {}

    def bind(self, abstract: type, concrete: type) -> None:
        
        with self._lock:
            self._bindings[abstract] = concrete

    def singleton(self, abstract: type, instance_or_factory: Any | Callable) -> None:
        
        with self._lock:
            if isinstance(instance_or_factory, type):

concrete = instance_or_factory

                def _lazy_factory(c, _abstract=abstract, _cls=concrete):

c._factories.pop(_abstract, None)
                    return c._resolve(_cls, set())

                self._factories[abstract] = _lazy_factory
            elif callable(instance_or_factory):

                self._factories[abstract] = instance_or_factory
            else:

                self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: type[Any]) -> Any:

scoped_instance = self._scope_context.resolve(abstract)
        if scoped_instance is not None:
            return scoped_instance
        return self._resolve(abstract, set())

    def scoped(self, abstract: type[Any], concrete: type[Any]) -> None:
        
        with self._lock:
            self._scoped_registry[abstract] = concrete

    def create_scope(self) -> ScopeContext:
        
        return ScopeContext(self._scoped_registry)

def _resolve(self, abstract: type[T] | Any, resolving: set[type]) -> T:

if abstract in self._instances:
            return self._instances[abstract]

factory = self._factories.get(abstract)
        if factory is not None:
            with self._lock:

                if abstract in self._instances:
                    return self._instances[abstract]
                if abstract in self._factories:
                    instance = self._factories[abstract](self)
                    self._instances[abstract] = instance
                    return instance

        concrete = self._bindings.get(abstract, abstract)

        if concrete in resolving:
            raise DependencyResolutionError(f"Circular dependency detected: {concrete}")

        if not inspect.isclass(concrete):
            raise DependencyResolutionError(f"Cannot resolve {abstract}")

        if getattr(concrete, "__abstractmethods__", None):
            raise DependencyResolutionError(
                f"Cannot instantiate abstract class {concrete}"
            )

        resolving.add(concrete)

        try:
            if getattr(concrete, "__init__", None) is object.__init__:
                return concrete()

cached_deps = self._resolution_cache.get(concrete)

            if cached_deps is None:
                try:
                    signature = inspect.signature(concrete.__init__)
                except ValueError:
                    with self._lock:
                        self._resolution_cache[concrete] = {}
                    return concrete()

                import typing

                try:
                    type_hints = typing.get_type_hints(concrete.__init__)
                except Exception:
                    type_hints = None

                cached_deps = {}
                for name, param in signature.parameters.items():
                    if name in ("self", "args", "kwargs"):
                        continue

                    annotation = inspect.Parameter.empty
                    if type_hints is not None and name in type_hints:
                        annotation = type_hints[name]
                    else:
                        annotation = param.annotation

                    if annotation == inspect.Parameter.empty:
                        raise DependencyResolutionError(
                            f"Missing type hint for parameter '{name}' in {concrete.__name__}"
                        )

                    cached_deps[name] = {
                        "annotation": annotation,
                        "has_default": param.default is not inspect.Parameter.empty,
                        "default": param.default,
                    }

                with self._lock:
                    self._resolution_cache[concrete] = cached_deps

            dependencies = {}
            for name, param_info in cached_deps.items():
                try:
                    dependencies[name] = self._resolve(
                        param_info["annotation"], resolving
                    )
                except Exception as e:
                    if param_info["has_default"]:
                        dependencies[name] = param_info["default"]
                    else:
                        raise DependencyResolutionError(
                            f"Failed to resolve '{name}' for {concrete.__name__}: {str(e)}"
                        )

            return concrete(**dependencies)
        finally:
            resolving.remove(concrete)
``````

# FILE: infrastructure/event_bus/__init__.py

```python
from .memory_event_bus import MemoryEventBus
from .thread_pool_event_bus import ThreadPoolEventBus
from .asyncio_event_bus import AsyncioEventBus
from .resilient_event_bus import ResilientEventBus
from .ipc_broker import IPCBroker
from .ipc_queue_event_bus import IPCQueueEventBus

__all__ = [
    "MemoryEventBus",
    "ThreadPoolEventBus",
    "AsyncioEventBus",
    "ResilientEventBus",
    "IPCBroker",
    "IPCQueueEventBus",
]
``````

# FILE: infrastructure/event_bus/asyncio_event_bus.py

```python
import asyncio
import inspect
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IAsyncEventBus, ILogger

class AsyncioEventBus(IAsyncEventBus):

def __init__(self, logger: ILogger | None = None) -> None:
        
        self._handlers: dict[str, tuple[Callable, ...]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    async def emit(self, event_name: str, data: Any = None) -> None:
        
        if self.logger:
            self.logger.info(f"Emitting async event: {event_name} with data: {data}")

handlers_snapshot = self._handlers.get(event_name, ())

        for handler in handlers_snapshot:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except asyncio.CancelledError as e:
                if self.logger:
                    self.logger.error(
                        f"Async handler cancelled for event {event_name}: {e}"
                    )
            except Exception as e:
                if self.logger:
                    self.logger.error(
                        f"Error executing async handler for event {event_name}: {e}"
                    )

    def on(self, event_name: str, handler: Callable) -> None:
        
        with self._lock:
            current_handlers = self._handlers.get(event_name, ())
            if handler not in current_handlers:
                self._handlers[event_name] = current_handlers + (handler,)

    def off(self, event_name: str, handler: Callable) -> None:
        
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name] = tuple(
                    h for h in self._handlers[event_name] if h != handler
                )
``````

# FILE: infrastructure/event_bus/ipc_broker.py

```python
import threading
import logging
import queue
from multiprocessing.queues import Queue
from sagittarius_engine.interfaces.i_logger import ILogger

class IPCBroker:

def __init__(self, publish_queue: Queue, logger: ILogger | None = None):
        self._publish_queue = publish_queue
        self._subscriber_queues: list[Queue] = []
        self._logger = logger
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def add_subscriber(self, sub_queue: Queue) -> None:
        
        with self._lock:
            if sub_queue not in self._subscriber_queues:
                self._subscriber_queues.append(sub_queue)

    def remove_subscriber(self, sub_queue: Queue) -> None:
        
        with self._lock:
            if sub_queue in self._subscriber_queues:
                self._subscriber_queues.remove(sub_queue)

    def start(self) -> None:
        
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="IPCBrokerThread"
        )
        self._thread.start()
        if self._logger:
            self._logger.info("IPCBroker started.")

    def stop(self) -> None:
        
        self._stop_event.set()
        try:
            self._publish_queue.put(("_STOP_", None))
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error stopping IPCBroker: {e}")
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._logger:
            self._logger.info("IPCBroker stopped.")

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                message = self._publish_queue.get(timeout=0.1)
                if (
                    isinstance(message, tuple)
                    and len(message) == 2
                    and (message[0] == "_STOP_")
                ):
                    break
                event_name, data = message
                with self._lock:
                    for sub_queue in self._subscriber_queues:
                        try:
                            sub_queue.put((event_name, data))
                        except Exception as e:
                            if self._logger:
                                self._logger.error(
                                    f"Failed to route event {event_name} to a subscriber: {e}"
                                )
                            else:
                                logging.error(
                                    f"Failed to route event {event_name} to a subscriber: {e}"
                                )
            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f"IPCBroker encountered an error: {e}")
                else:
                    logging.error(f"IPCBroker encountered an error: {e}")
``````

# FILE: infrastructure/event_bus/ipc_queue_event_bus.py

```python
import threading
import logging
import queue
from collections.abc import Callable
from multiprocessing.queues import Queue
from typing import Any
from sagittarius_engine.interfaces.i_event_bus import IEventBus
from sagittarius_engine.interfaces.i_logger import ILogger

class IPCQueueEventBus(IEventBus):

def __init__(
        self,
        subscriber_queue: Queue | None = None,
        publish_queue: Queue | None = None,
        logger: ILogger | None = None,
    ):
        self._subscriber_queue = subscriber_queue
        self._publish_queue = publish_queue
        self._logger = logger
        self._handlers: dict[str, tuple[Callable, ...]] = {}
        self._handlers_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = type(event_name_or_obj).__qualname__
            payload = data if data is not None else event_name_or_obj
        if not self._publish_queue:
            if self._logger:
                self._logger.warning(
                    f"Cannot emit '{event_name}': publish_queue is None."
                )
            else:
                logging.warning(f"Cannot emit '{event_name}': publish_queue is None.")
            return
        try:
            self._publish_queue.put((event_name, payload))
        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Failed to emit event '{event_name}' to publish_queue: {e}"
                )
            else:
                logging.error(
                    f"Failed to emit event '{event_name}' to publish_queue: {e}"
                )

    def on(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        event_name = (
            event_name_or_type
            if isinstance(event_name_or_type, str)
            else getattr(event_name_or_type, "__name__", str(event_name_or_type))
        )
        with self._handlers_lock:
            current_handlers = self._handlers.get(event_name, ())
            if handler not in current_handlers:
                self._handlers[event_name] = current_handlers + (handler,)

    def off(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        event_name = (
            event_name_or_type
            if isinstance(event_name_or_type, str)
            else getattr(event_name_or_type, "__name__", str(event_name_or_type))
        )
        with self._handlers_lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name] = tuple(
                    h for h in self._handlers[event_name] if h != handler
                )

    def start(self) -> None:
        
        if not self._subscriber_queue:
            if self._logger:
                self._logger.warning(
                    "No subscriber_queue provided; IPCQueueEventBus will not listen for events."
                )
            return
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="IPCQueueEventBusListener"
        )
        self._thread.start()
        if self._logger:
            self._logger.info("IPCQueueEventBus listener started.")

    def stop(self) -> None:
        
        self._stop_event.set()
        if self._subscriber_queue:
            try:
                self._subscriber_queue.put(("_STOP_", None))
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Error stopping IPCQueueEventBus: {e}")
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._logger:
            self._logger.info("IPCQueueEventBus listener stopped.")

    def _run(self) -> None:
        if not self._subscriber_queue:
            return
        while not self._stop_event.is_set():
            try:
                message = self._subscriber_queue.get(timeout=0.1)
                if (
                    isinstance(message, tuple)
                    and len(message) == 2
                    and (message[0] == "_STOP_")
                ):
                    break
                event_name, data = message
                self._dispatch(event_name, data)
            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f"IPCQueueEventBus listener error: {e}")

    def _dispatch(self, event_name: str, data: Any) -> None:

handlers = self._handlers.get(event_name, ())
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Error in IPC handler for '{event_name}': {e}")
``````

# FILE: infrastructure/event_bus/memory_event_bus.py

```python
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IEventBus, ILogger

class MemoryEventBus(IEventBus):

def __init__(self, logger: ILogger | None = None) -> None:
        
        self._handlers: dict[str, tuple[Callable, ...]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    def _get_event_key(self, event_name_or_type: str | type | Any) -> str:
        if isinstance(event_name_or_type, str):
            return event_name_or_type
        key = getattr(event_name_or_type, "event_name", None)
        if key:
            return key
        if isinstance(event_name_or_type, type):
            return event_name_or_type.__qualname__
        return event_name_or_type.__class__.__qualname__

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = self._get_event_key(event_name_or_obj)
            payload = data if data is not None else event_name_or_obj

        if self.logger:
            self.logger.info(f"Emitting event: {event_name} with data: {payload}")

handlers_snapshot = self._handlers.get(event_name, ())

        for handler in handlers_snapshot:
            try:
                handler(payload)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in handler {handler}: {e}")

    def on(self, event_name_or_type: str | type | Any, handler: Callable) -> None:
        
        key = self._get_event_key(event_name_or_type)
        with self._lock:
            current_handlers = self._handlers.get(key, ())
            if handler not in current_handlers:
                self._handlers[key] = current_handlers + (handler,)

    def off(self, event_name_or_type: str | type | Any, handler: Callable) -> None:
        
        key = self._get_event_key(event_name_or_type)
        with self._lock:
            if key in self._handlers and handler in self._handlers[key]:
                self._handlers[key] = tuple(
                    h for h in self._handlers[key] if h != handler
                )

    def get_handlers(
        self, event_name_or_type: str | type | Any
    ) -> tuple[Callable, ...]:
        
        key = self._get_event_key(event_name_or_type)
        return self._handlers.get(key, ())
``````

# FILE: infrastructure/event_bus/resilient_event_bus.py

```python
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IEventBus, ILogger

class ResilientEventBus(IEventBus):

def __init__(
        self, inner_bus: IEventBus, max_retries: int = 3, logger: ILogger | None = None
    ) -> None:
        
        self.inner_bus = inner_bus
        self.max_retries = max_retries
        self._dlq: list[tuple[str, Any, Callable, Exception]] = []
        self.logger = logger

        self._wrapper_map: dict[tuple[str, Callable], Callable] = {}
        self._lock = threading.Lock()

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = (
                getattr(
                    event_name_or_obj,
                    "event_name",
                    type(event_name_or_obj).__qualname__,
                )
                or type(event_name_or_obj).__qualname__
            )
            payload = data if data is not None else event_name_or_obj

        if self.logger:
            self.logger.info(
                f"Emitting resilient event: {event_name} with data: {payload}"
            )

        self.inner_bus.emit(event_name_or_obj, data)

    def on(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        event_name = (
            event_name_or_type
            if isinstance(event_name_or_type, str)
            else getattr(event_name_or_type, "__name__", str(event_name_or_type))
        )

        with self._lock:
            key = (event_name, handler)
            if key in self._wrapper_map:
                return

            def resilient_wrapper(data: Any) -> None:
                for attempt in range(self.max_retries + 1):
                    try:
                        handler(data)
                        break
                    except Exception as e:
                        if attempt == self.max_retries:
                            with self._lock:
                                self._dlq.append((event_name, data, handler, e))

            self._wrapper_map[key] = resilient_wrapper

        self.inner_bus.on(event_name_or_type, resilient_wrapper)

    def off(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        event_name = (
            event_name_or_type
            if isinstance(event_name_or_type, str)
            else getattr(event_name_or_type, "__name__", str(event_name_or_type))
        )

        with self._lock:
            key = (event_name, handler)
            wrapper = self._wrapper_map.pop(key, None)

        if wrapper:
            self.inner_bus.off(event_name_or_type, wrapper)

    def get_dlq(self) -> list[tuple[str, Any, Callable, Exception]]:
        
        with self._lock:
            return list(self._dlq)

    def reprocess(self) -> None:
        
        with self._lock:
            current_dlq = self._dlq
            self._dlq = []
        for event_name, data, handler, _ in current_dlq:
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        with self._lock:
                            self._dlq.append((event_name, data, handler, e))
``````

# FILE: infrastructure/event_bus/thread_pool_event_bus.py

```python
import concurrent.futures
from collections.abc import Callable
from typing import Any

from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.interfaces import IEventBus, ILogger

class ThreadPoolEventBus(IEventBus):

def __init__(self, max_workers: int = 4, logger: ILogger | None = None) -> None:
        
        self._inner_bus = MemoryEventBus(
            logger=None
        )
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logger

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = (
                getattr(
                    event_name_or_obj,
                    "event_name",
                    type(event_name_or_obj).__qualname__,
                )
                or type(event_name_or_obj).__qualname__
            )
            payload = data if data is not None else event_name_or_obj
        if self.logger:
            self.logger.info(
                f"Emitting event: {event_name} to ThreadPoolEventBus with data: {payload}"
            )

if hasattr(self._inner_bus, "get_handlers"):
            handlers_snapshot = self._inner_bus.get_handlers(
                event_name_or_obj
                if not isinstance(event_name_or_obj, str)
                else event_name
            )
        else:
            handlers_snapshot = getattr(self._inner_bus, "_handlers", {}).get(
                event_name, ()
            )

        futures = []
        for handler in handlers_snapshot:
            futures.append(self._executor.submit(handler, payload))

        for future in futures:

            def _log_error(f, event=event_name):
                try:
                    f.result()
                except Exception as exc:
                    if self.logger:
                        self.logger.error(
                            f"Error executing handler for event {event}: {exc}"
                        )

            future.add_done_callback(_log_error)

    def on(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        self._inner_bus.on(event_name_or_type, handler)

    def off(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        
        self._inner_bus.off(event_name_or_type, handler)

    def shutdown(self, wait: bool = True) -> None:
        
        self._executor.shutdown(wait=wait)

    def get_handlers(
        self, event_name_or_type: str | Any
    ) -> tuple[Callable[..., Any], ...]:
        
        if hasattr(self._inner_bus, "get_handlers"):
            return self._inner_bus.get_handlers(event_name_or_type)
        return ()
``````

# FILE: infrastructure/logging/__init__.py

```python
from .std_logger import StdLogger
from .log_metrics import LogMetrics
from .tcp_log_viewer_handler import TcpLogViewerHandler
from .logger_config import LoggerConfig

__all__ = [
    "StdLogger",
    "LogMetrics",
    "TcpLogViewerHandler",
    "LoggerConfig",
]
``````

# FILE: infrastructure/logging/log_metrics.py

```python
import json

from sagittarius_engine.interfaces import ILogger
from sagittarius_engine.interfaces.i_metrics import IMetrics

class LogMetrics(IMetrics):

def __init__(self, logger: ILogger) -> None:
        
        self.logger = logger

    def _format_tags(self, tags: dict[str, str] | None) -> str:
        if not tags:
            return ""
        return " " + json.dumps(tags)

    def increment_counter(
        self, name: str, value: int = 1, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=counter name={name} value={value}{tag_str}")

    def record_timing(
        self, name: str, duration_ms: float, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(
            f"[METRIC] type=timing name={name} duration_ms={duration_ms}{tag_str}"
        )

    def set_gauge(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=gauge name={name} value={value}{tag_str}")
``````

# FILE: infrastructure/logging/logger_config.py

```python
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces import IConfig

@dataclass(frozen=True)
class LoggerConfig:

log_level: int = logging.INFO

log_file: str | None = None

console_enabled: bool = True

viewer_enabled: bool = False
    viewer_host: str = "localhost"
    viewer_port: int = 9999
    viewer_module: str = "sagittarius-app"

    @staticmethod
    def from_iconfig(config: "IConfig") -> "LoggerConfig":
        
        level_str: str = config.get("log.level", "INFO").upper()

        log_level: int = getattr(logging, level_str, logging.INFO)

        return LoggerConfig(
            log_level=log_level,
            log_file=config.get("log.file"),
            console_enabled=config.get("log.console.enabled", True),
            viewer_enabled=config.get("log.viewer.enabled", False),
            viewer_host=config.get("log.viewer.host", "localhost"),
            viewer_port=config.get("log.viewer.port", 9999),
            viewer_module=config.get("log.viewer.module", "sagittarius-app"),
        )
``````

# FILE: infrastructure/logging/std_logger.py

```python
import logging
import sys
from typing import Any

from sagittarius_engine.infrastructure.logging.logger_config import LoggerConfig
from sagittarius_engine.infrastructure.logging.tcp_log_viewer_handler import (
    TcpLogViewerHandler,
)
from sagittarius_engine.interfaces import IConfig, ILogger

class StdLogger(ILogger):

def __init__(self, config: IConfig | None = None):
        
        self._logger = logging.getLogger("App")

cfg: LoggerConfig = (
            LoggerConfig.from_iconfig(config) if config else LoggerConfig()
        )

self._logger.setLevel(cfg.log_level)

        for handler in list(self._logger.handlers):
            handler.close()
            self._logger.removeHandler(handler)

        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if cfg.console_enabled:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)

        if cfg.log_file:
            fh = logging.FileHandler(cfg.log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        if cfg.viewer_enabled:
            vh = TcpLogViewerHandler(
                host=cfg.viewer_host,
                port=cfg.viewer_port,
                module_name=cfg.viewer_module,
            )
            self._logger.addHandler(vh)

    def _format_extra(self, extra: dict[str, Any] | None) -> dict[str, Any]:
        return {"extra": extra} if extra is not None else {}

    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        self._logger.info(message, extra=self._format_extra(extra))

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        self._logger.warning(message, extra=self._format_extra(extra))

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        self._logger.error(message, extra=self._format_extra(extra))

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        self._logger.debug(message, extra=self._format_extra(extra))
``````

# FILE: infrastructure/logging/tcp_log_viewer_handler.py

```python
import json
import logging
import queue
import socket
import threading
import time
from datetime import datetime, timezone
from typing import Any

class TcpLogViewerHandler(logging.Handler):

def __init__(
        self,
        host: str = "localhost",
        port: int = 9999,
        module_name: str = "sagittarius-app",
        max_queue_size: int = 10000,
    ) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.module_name = module_name
        self._queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._seq = 0

        self._worker_thread = threading.Thread(
            target=self._network_worker,
            name="Sagittarius-TcpLogWorker",
            daemon=True,
        )
        self._worker_thread.start()

    def emit(self, record: logging.LogRecord) -> None:
        
        try:
            raw_extra = getattr(record, "extra", {})
            if isinstance(raw_extra, dict):
                extra_data = raw_extra.copy()
            else:
                extra_data = {"raw_extra": str(raw_extra)} if raw_extra else {}

            self._seq += 1
            index = extra_data.pop("index", self._seq)

            submodule = extra_data.pop("submodule", None)
            if (
                not submodule
                and hasattr(record, "submodule")
                and getattr(record, "submodule")
            ):
                submodule = getattr(record, "submodule")

            msg = record.getMessage()

if not submodule and msg.startswith("[") and "]" in msg:
                bracket_content = msg[1 : msg.find("]")]
                if " " not in bracket_content:
                    submodule = bracket_content

            if not submodule and record.name and record.name != "App":
                submodule = record.name

            dt = datetime.fromtimestamp(record.created, tz=timezone.utc)

            payload: dict[str, Any] = {
                "index": index,
                "timestamp": dt.isoformat(),
                "level": record.levelname,
                "message": msg,
                "module": self.module_name,
                "submodule": submodule,
                "extra": extra_data,
            }

            self._queue.put_nowait(payload)
        except queue.Full:

            pass
        except Exception:
            self.handleError(record)

    def _network_worker(self) -> None:
        sock: socket.socket | None = None
        while not self._stop_event.is_set():
            try:
                payload = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            data_bytes = (json.dumps(payload) + "\n").encode("utf-8")
            sent = False

            while not sent and not self._stop_event.is_set():
                try:
                    if sock is None:
                        sock = socket.create_connection(
                            (self.host, self.port), timeout=2.0
                        )
                    sock.sendall(data_bytes)
                    sent = True
                except (OSError, socket.error):
                    if sock:
                        try:
                            sock.close()
                        except Exception as e:
                            import logging
                            logging.getLogger(__name__).error(f"Socket close error: {e}")
                        sock = None

                    time.sleep(1.0)
                    break

        if sock:
            try:
                sock.close()
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Socket close error: {e}")

    def close(self) -> None:
        
        self._stop_event.set()
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)
        super().close()
``````

# FILE: infrastructure/persistence/__init__.py

```python
from .i_thread_manager import IThreadManager

__all__ = [
    "IThreadManager",
]
``````

# FILE: infrastructure/storage/__init__.py

```python
from .local_file_storage import LocalFileStorage
from .s3_file_storage import S3FileStorage
from .azure_blob_storage import AzureBlobStorage

__all__ = [
    "LocalFileStorage",
    "S3FileStorage",
    "AzureBlobStorage",
]
``````

# FILE: infrastructure/storage/azure_blob_storage.py

```python
from sagittarius_engine.interfaces.i_file_storage import IFileStorage

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.storage.blob import BlobServiceClient

    AZURE_INSTALLED = True
except ImportError:
    AZURE_INSTALLED = False

class AzureBlobStorage(IFileStorage):

def __init__(self, connection_string: str, container_name: str) -> None:
        
        if not AZURE_INSTALLED:
            raise ImportError(
                "azure-storage-blob is not installed. Please install it using `pip install azure-storage-blob`."
            )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )

    def read(self, path: str) -> bytes:
        
        blob_client = self.container_client.get_blob_client(path)
        return blob_client.download_blob().readall()

    def write(self, path: str, data: bytes | str) -> None:
        
        blob_client = self.container_client.get_blob_client(path)
        body = data.encode("utf-8") if isinstance(data, str) else data
        blob_client.upload_blob(body, overwrite=True)

    def delete(self, path: str) -> None:
        
        blob_client = self.container_client.get_blob_client(path)
        blob_client.delete_blob()

    def exists(self, path: str) -> bool:
        
        blob_client = self.container_client.get_blob_client(path)
        try:
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False
``````

# FILE: infrastructure/storage/local_file_storage.py

```python
import os

from sagittarius_engine.interfaces.i_file_storage import IFileStorage
from sagittarius_engine.exceptions import PathTraversalError

class LocalFileStorage(IFileStorage):

def __init__(self, base_path: str = "") -> None:
        
        self.base_path = base_path

    def _get_full_path(self, path: str) -> str:
        if path is None:
            raise ValueError("Path cannot be None")

        base_path_real = os.path.realpath(self.base_path)
        full_path = os.path.join(self.base_path, path)
        full_path_real = os.path.realpath(full_path)

        if os.path.commonpath([base_path_real, full_path_real]) != base_path_real:
            raise PathTraversalError(f"Path traversal detected: {path}")

        return full_path_real

    def read(self, path: str) -> bytes:
        
        full_path = self._get_full_path(path)
        with open(full_path, "rb") as f:
            return f.read()

    def write(self, path: str, data: bytes | str) -> None:
        
        full_path = self._get_full_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        mode = "wb" if isinstance(data, bytes) else "w"
        with open(full_path, mode) as f:
            f.write(data)

    def delete(self, path: str) -> None:
        
        full_path = self._get_full_path(path)
        if os.path.exists(full_path):
            os.remove(full_path)

    def exists(self, path: str) -> bool:
        
        return os.path.exists(self._get_full_path(path))
``````

# FILE: infrastructure/storage/s3_file_storage.py

```python
from sagittarius_engine.interfaces.i_file_storage import IFileStorage

try:
    import boto3
    from botocore.exceptions import ClientError

    BOTO3_INSTALLED = True
except ImportError:
    BOTO3_INSTALLED = False

class S3FileStorage(IFileStorage):

def __init__(self, bucket_name: str) -> None:
        
        if not BOTO3_INSTALLED:
            raise ImportError(
                "boto3 is not installed. Please install it using `pip install boto3`."
            )
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def read(self, path: str) -> bytes:
        
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=path)
        return response["Body"].read()

    def write(self, path: str, data: bytes | str) -> None:
        
        body = data.encode("utf-8") if isinstance(data, str) else data
        self.s3_client.put_object(Bucket=self.bucket_name, Key=path, Body=body)

    def delete(self, path: str) -> None:
        
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)

    def exists(self, path: str) -> bool:
        
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise
``````

# FILE: infrastructure/thread_manager.py

```python
import concurrent.futures
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces.i_thread_manager import (
    IThreadManager,
)

class ThreadManager(IThreadManager):

def __init__(self, max_workers: int = 4) -> None:
        
        self._max_workers = max_workers
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_workers
        )
        self._lock = threading.Lock()

    def submit(
        self, task: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> concurrent.futures.Future[Any]:
        
        with self._lock:
            return self._executor.submit(task, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        
        with self._lock:
            self._executor.shutdown(wait=wait)
``````

# FILE: interfaces/__init__.py

```python
from .i_module import IModule
from .i_extension import IExtension
from .i_engine_context import IEngineContext
from .i_task_manager import ITaskHandle, ITaskManager
from .i_event_bus import IEventBus
from .i_async_event_bus import IAsyncEventBus
from .i_container import IContainer
from .i_middleware import IMiddleware
from .i_logger import ILogger
from .i_config import IConfig
from .i_input_port import IInputPort
from .i_output_port import IOutputPort
from .i_dispatchable import IDispatchable

__all__ = [
    "IModule",
    "IExtension",
    "IEngineContext",
    "ITaskHandle",
    "ITaskManager",
    "IEventBus",
    "IAsyncEventBus",
    "IContainer",
    "IMiddleware",
    "ILogger",
    "IConfig",
    "IInputPort",
    "IOutputPort",
    "IDispatchable",
    "IThreadManager",
    "IFileStorage",
    "IMetrics",
]

from .i_thread_manager import IThreadManager
from .i_file_storage import IFileStorage
from .i_metrics import IMetrics
``````

# FILE: interfaces/i_async_event_bus.py

```python
from collections.abc import Callable
from typing import Any, Protocol

class IAsyncEventBus(Protocol):

async def emit(self, event_name: str, data: Any = None) -> None:
        
        ...

    def on(self, event_name: str, handler: Callable) -> None:
        
        ...

    def off(self, event_name: str, handler: Callable) -> None:
        
        ...
``````

# FILE: interfaces/i_config.py

```python
from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")

class IConfig(ABC):

@abstractmethod
    def get(self, key: str, default: Any = None, cast: type[T] | None = None) -> Any:
        
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        
        ...
``````

# FILE: interfaces/i_container.py

```python
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Generator, TypeVar

T = TypeVar("T", bound=Any)

class IContainer(ABC):

@abstractmethod
    def bind(self, abstract: type[Any], concrete: type[Any]) -> None:
        
        ...

    @abstractmethod
    def singleton(
        self,
        abstract: type[Any],
        instance_or_factory: Any,
    ) -> None:
        
        ...

    @abstractmethod
    def resolve(self, abstract: type[Any]) -> Any:
        
        ...

    @abstractmethod
    def scoped(self, abstract: type[Any], concrete: type[Any]) -> None:
        
        ...

    @abstractmethod
    def create_scope(self) -> Any:
        
        ...
``````

# FILE: interfaces/i_dispatchable.py

```python
from typing import Any, TypeVar

TResult_co = TypeVar("TResult_co", covariant=True)

class IDispatchable:

def execute(self, dto: Any) -> Any:
        
        ...
``````

# FILE: interfaces/i_engine_context.py

```python
from abc import ABC, abstractmethod
from sagittarius_engine.interfaces.i_container import IContainer
from sagittarius_engine.interfaces.i_event_bus import IEventBus
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_task_manager import ITaskManager

class IEngineContext(ABC):

@property
    @abstractmethod
    def container(self) -> IContainer:
        
        ...

    @property
    @abstractmethod
    def event_bus(self) -> IEventBus:
        
        ...

    @property
    @abstractmethod
    def logger(self) -> ILogger | None:
        
        ...

    @property
    @abstractmethod
    def tasks(self) -> ITaskManager:
        
        ...
``````

# FILE: interfaces/i_event_bus.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

from sagittarius_engine.domain.base_event import BaseEvent

E = TypeVar("E", bound=BaseEvent)

class IEventBus(ABC):

@abstractmethod
    def emit(self, event_name_or_obj: str | BaseEvent | Any, data: Any = None) -> None:
        
        ...

    @abstractmethod
    def on(
        self, event_name_or_type: str | type[E] | Any, handler: Callable[..., Any]
    ) -> None:
        
        ...

    @abstractmethod
    def off(
        self, event_name_or_type: str | type[E] | Any, handler: Callable[..., Any]
    ) -> None:
        
        ...

    def get_handlers(
        self, event_name_or_type: str | type[E] | Any
    ) -> tuple[Callable[..., Any], ...]:
        
        return ()
``````

# FILE: interfaces/i_extension.py

```python
from abc import ABC, abstractmethod
from collections.abc import Coroutine
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

@dataclass
class ExtensionDescriptor:

name: str
    version: str = "1.0.0"
    dependencies: list[str] = field(default_factory=list)
    optional_dependencies: list[str] = field(default_factory=list)
    enabled: bool = True
    priority: int = 0
    author: str = ""
    description: str = ""

class IExtension(ABC):

@property
    def descriptor(self) -> ExtensionDescriptor:
        
        deps = getattr(self, "dependencies", [])
        opt_deps = getattr(self, "optional_dependencies", [])
        prio = getattr(self, "priority", 0)
        enabled = getattr(self, "enabled", True)
        return ExtensionDescriptor(
            name=self.__class__.__name__,
            dependencies=deps if isinstance(deps, list) else [],
            optional_dependencies=opt_deps if isinstance(opt_deps, list) else [],
            priority=prio if isinstance(prio, int) else 0,
            enabled=enabled if isinstance(enabled, bool) else True,
        )
    
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def register(self, context: "IEngineContext") -> None:
        
        ...

    @abstractmethod
    def boot(self, context: "IEngineContext") -> None:
        
        ...

    @abstractmethod
    def shutdown(self, context: "IEngineContext") -> None:
        
        ...

    def initialize(self, context: "IEngineContext") -> None:
        
        self.register(context)

    def start(self, context: "IEngineContext") -> None:
        
        self.boot(context)

    def stop(self, context: "IEngineContext") -> None:
        
        self.shutdown(context)

    def dispose(self, context: "IEngineContext") -> None:
        
        pass

    async def boot_async(self, context: "IEngineContext") -> None:
        
        return

    async def shutdown_async(self, context: "IEngineContext") -> None:
        
        return
``````

# FILE: interfaces/i_file_storage.py

```python
from abc import ABC, abstractmethod

class IFileStorage(ABC):

@abstractmethod
    def read(self, path: str) -> bytes:
        
        ...

    @abstractmethod
    def write(self, path: str, data: bytes | str) -> None:
        
        ...

    @abstractmethod
    def delete(self, path: str) -> None:
        
        ...

    @abstractmethod
    def exists(self, path: str) -> bool:
        
        ...
``````

# FILE: interfaces/i_input_port.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IInputPort(ABC):

@abstractmethod
    def receive(self) -> dict[str, Any]:
        
        pass
``````

# FILE: interfaces/i_logger.py

```python
from abc import ABC, abstractmethod
from typing import Any

class ILogger(ABC):

@abstractmethod
    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        ...

    @abstractmethod
    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        ...

    @abstractmethod
    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        ...

    @abstractmethod
    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        
        ...
``````

# FILE: interfaces/i_metrics.py

```python
from abc import ABC, abstractmethod

class IMetrics(ABC):

@abstractmethod
    def increment_counter(
        self, name: str, value: int = 1, tags: dict[str, str] | None = None
    ) -> None:
        
        ...

    @abstractmethod
    def record_timing(
        self, name: str, duration_ms: float, tags: dict[str, str] | None = None
    ) -> None:
        
        ...

    @abstractmethod
    def set_gauge(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        
        ...
``````

# FILE: interfaces/i_middleware.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

class IMiddleware(ABC):

@abstractmethod
    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        ...
``````

# FILE: interfaces/i_module.py

```python
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel import App

class IModule(ABC):

@abstractmethod
    def register(self, app: "App") -> None:
        
        ...

    @abstractmethod
    def boot(self, app: "App") -> None:
        
        ...
``````

# FILE: interfaces/i_output_port.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IOutputPort(ABC):

@abstractmethod
    def present(self, result: Any) -> None:
        
        pass

    @abstractmethod
    def present_error(self, error: Exception) -> None:
        
        pass
``````

# FILE: interfaces/i_task_manager.py

```python
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
    from sagittarius_engine.runtime.tasks.background_task import TaskState

class ITaskHandle(ABC):

@property
    @abstractmethod
    def id(self) -> str:
        
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        
        ...

    @property
    @abstractmethod
    def token(self) -> "CancellationToken":
        
        ...

    @property
    @abstractmethod
    def future(self) -> Optional[Any]:
        
        ...

    @property
    @abstractmethod
    def status(self) -> "TaskState":
        
        ...

    @property
    @abstractmethod
    def progress(self) -> float:
        
        ...

    @abstractmethod
    def cancel(self) -> None:
        
        ...

class ITaskManager(ABC):

@abstractmethod
    def spawn(
        self,
        callable_or_coro: Callable[..., Any] | Any,
        name: Optional[str] = None,
        token: Optional["CancellationToken"] = None,
        critical: bool = False,
    ) -> ITaskHandle:
        
        ...

    @abstractmethod
    def shutdown(self, timeout: float = 5.0) -> None:
        
        ...
``````

# FILE: interfaces/i_thread_manager.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
import concurrent.futures
from typing import Any

class IThreadManager(ABC):

@abstractmethod
    def submit(
        self, task: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> concurrent.futures.Future[Any]:
        
        pass

    @abstractmethod
    def shutdown(self, wait: bool = True) -> None:
        
        pass
``````

# FILE: kernel/__init__.py

```python
from .app import App
from .context import EngineContext
from .app_runner import ApplicationRunner
from .middleware_pipeline import MiddlewarePipeline
from .module_auto_discovery import ModuleAutoDiscovery
from .lifecycle import EngineLifecycle
from .module_loader import ModuleLoader
from .bootstrap import Bootstrap
from .dispatcher import Dispatcher

__all__ = [
    "App",
    "EngineContext",
    "ApplicationRunner",
    "MiddlewarePipeline",
    "ModuleAutoDiscovery",
    "EngineLifecycle",
    "ModuleLoader",
    "Bootstrap",
    "Dispatcher",
]
``````

# FILE: kernel/app_runner.py

```python
from collections.abc import Mapping
from typing import Any

from sagittarius_engine.kernel import App
from sagittarius_engine.interfaces.i_input_port import IInputPort
from sagittarius_engine.interfaces.i_output_port import IOutputPort

COMMAND_KEY = "command"
EXIT_COMMAND = "exit"

class ApplicationRunner:

def __init__(
        self, app: App, input_port: IInputPort, output_port: IOutputPort
    ) -> None:
        self.app = app
        self.input_port = input_port
        self.output_port = output_port

    def run_cli_loop(
        self,
        command_map: Mapping[str, type] | None = None,
        query_map: Mapping[str, type] | None = None,
    ) -> None:
        
        cmd_map = command_map or {}
        q_map = query_map or {}

        while True:
            try:
                data = self.input_port.receive()
                if not data:
                    break

                command_name = data.get(COMMAND_KEY)
                if not isinstance(command_name, str) or command_name == EXIT_COMMAND:
                    break

                if command_name in cmd_map:
                    cmd_class = cmd_map[command_name]
                    result = self.execute(cmd_class, data)
                    self.output_port.present(result)
                elif command_name in q_map:
                    query_class = q_map[command_name]
                    result = self.query(query_class, data)
                    self.output_port.present(result)
                else:
                    self.output_port.present_error(
                        ValueError(f"Unknown command: {command_name}")
                    )

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.output_port.present_error(e)

    def execute(self, command_class: type, dto: object | None = None) -> Any:
        
        return self.app.dispatch(command_class, dto)

    def query(self, query_class: type, dto: object | None = None) -> Any:
        
        return self.app.dispatch(query_class, dto)
``````

# FILE: kernel/app.py

```python
from typing import TypeVar, Any
from sagittarius_engine.exceptions import ModuleRegistrationError
from sagittarius_engine.interfaces.i_dispatchable import IDispatchable

from sagittarius_engine.kernel.context import EngineContext
from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
from sagittarius_engine.kernel.lifecycle import EngineLifecycle
from sagittarius_engine.interfaces import (
    IContainer,
    IEventBus,
    IExtension,
    ILogger,
    IMiddleware,
    IModule,
)

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

class App:

def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        
        self.context = EngineContext(self, container, event_bus)

    @property
    def container(self) -> IContainer:
        return self.context.container

    @property
    def event_bus(self) -> IEventBus:
        return self.context.event_bus

    @property
    def modules(self) -> list[IExtension]:
        return self.context.modules

    @property
    def pipeline(self) -> MiddlewarePipeline:
        return self.context.middleware_pipeline

    @property
    def lifecycle(self) -> EngineLifecycle:
        return self.context.lifecycle

    def use(self, extension_or_module: IExtension | IModule) -> None:
        
        try:
            self.context.extension_manager.register(extension_or_module)
        except TypeError as e:
            raise ModuleRegistrationError(str(e)) from e

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        
        self.context.middleware_pipeline.add(middleware_instance)

    def _get_logger(self) -> ILogger:
        return self.context.logger

    def boot(self, auto_discover: str | None = None) -> None:
        
        self.context.bootstrap.boot(auto_discover)

    def dispatch(self, handler_class: type[IDispatchable], input_dto: object | None = None) -> Any:
        
        return self.context.dispatcher.dispatch(handler_class, input_dto)

    def execute(self, command_class: type, input_dto: object | None = None) -> Any:
        
        import warnings

        warnings.warn(
            "App.execute is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: object | None = None) -> Any:
        
        import warnings

        warnings.warn(
            "App.query is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)

    def stop(self) -> None:
        
        if self.context.lifecycle.is_stopping or self.context.lifecycle.is_stopped:
            return

        logger = self._get_logger()
        logger.info("App is stopping gracefully...")

        self.context.lifecycle.set_stopping()

try:
            self.context.scheduler.stop()
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

try:
            self.context.hosted_services.stop()
        except Exception as e:
            logger.error(f"Error stopping hosted services: {e}")

try:
            self.context.extension_manager.stop_and_dispose()
        except Exception as e:
            logger.error(f"Error stopping extensions: {e}")

try:
            self.context.tasks.shutdown()
        except Exception as e:
            logger.error(f"Error shutting down task manager: {e}")

try:
            self.context.async_runtime.stop()
        except Exception as e:
            logger.error(f"Error stopping async runtime: {e}")

try:
            bus = self.context.event_bus
            if hasattr(bus, "shutdown") and callable(getattr(bus, "shutdown")):
                bus.shutdown()
            elif hasattr(bus, "dispose") and callable(getattr(bus, "dispose")):
                bus.dispose()
        except Exception as e:
            logger.error(f"Error shutting down event bus: {e}")

        self.context.lifecycle.set_stopped()
        logger.info("App stopped.")
``````

# FILE: kernel/bootstrap.py

```python
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext
from sagittarius_engine.interfaces import ILogger

class Bootstrap:

def __init__(self, context: "IKernelContext") -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def boot(self, auto_discover: Optional[str] = None) -> None:
        
        logger = self._get_logger()
        if logger:
            logger.info("App is booting...")

        self.context.lifecycle.set_booting()

self.context.async_runtime.start()

        try:
            if auto_discover:
                self.context.module_loader.discover_and_load(auto_discover)

            self.context.extension_manager.initialize_and_start()

self.context.hosted_services.start()

self.context.scheduler.start()

        except (RuntimeError, ValueError, TypeError, AttributeError, ImportError, OSError) as e:
            if logger:
                logger.error(
                    f"[Bootstrap] Error during boot sequence: {e}. Shutting down runtime..."
                )

            try:
                self.context.scheduler.stop()
            except (RuntimeError, ValueError) as se:
                if logger:
                    logger.warning(
                        f"[Bootstrap] Error stopping scheduler during boot cleanup: {se}"
                    )
            try:
                self.context.hosted_services.stop()
            except (RuntimeError, ValueError) as he:
                if logger:
                    logger.warning(
                        f"[Bootstrap] Error stopping hosted services during boot cleanup: {he}"
                    )
            try:
                self.context.async_runtime.stop()
            except (RuntimeError, ValueError) as ae:
                if logger:
                    logger.warning(
                        f"[Bootstrap] Error stopping async runtime during boot cleanup: {ae}"
                    )
            raise e

        self.context.lifecycle.set_booted()

        if logger:
            logger.info(
                f"App booted successfully with {len(self.context.modules)} modules."
            )

        self.context.event_bus.emit("app.booted", self.context.app)
``````

# FILE: kernel/context.py

```python
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App
from sagittarius_engine.interfaces import (
    IContainer,
    IEventBus,
    ILogger,
    IConfig,
    ITaskManager,
)
from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
from sagittarius_engine.kernel.lifecycle import EngineLifecycle
from sagittarius_engine.kernel.module_loader import ModuleLoader
from sagittarius_engine.kernel.bootstrap import Bootstrap
from sagittarius_engine.kernel.dispatcher import Dispatcher
from sagittarius_engine.kernel.i_kernel_context import IKernelContext
from sagittarius_engine.kernel.extension_manager import ExtensionManager

class EngineContext(IKernelContext):

def __init__(self, app: "App", container: IContainer, event_bus: IEventBus) -> None:
        self.app = app
        self._container = container
        self._event_bus = event_bus
        self.middleware_pipeline = MiddlewarePipeline()
        self.extension_manager = ExtensionManager(self)

self.lifecycle = EngineLifecycle(self)
        self.module_loader = ModuleLoader(self)
        self.bootstrap = Bootstrap(self)
        self.dispatcher = Dispatcher(self)

from sagittarius_engine.runtime.async_runtime.async_runtime import AsyncRuntime
        from sagittarius_engine.runtime.tasks.task_manager import TaskManager
        from sagittarius_engine.runtime.scheduler.scheduler import Scheduler
        from sagittarius_engine.runtime.hosted.hosted_service_manager import (
            HostedServiceManager,
        )

        self.async_runtime = AsyncRuntime(self)
        self._tasks: ITaskManager = TaskManager(self)
        self.scheduler = Scheduler(self)
        self.hosted_services = HostedServiceManager(self)

self._container.singleton(AsyncRuntime, self.async_runtime)
        self._container.singleton(TaskManager, self._tasks)
        self._container.singleton(Scheduler, self.scheduler)
        self._container.singleton(HostedServiceManager, self.hosted_services)

    @property
    def container(self) -> IContainer:
        return self._container

    @container.setter
    def container(self, value: IContainer) -> None:
        self._container = value

    @property
    def event_bus(self) -> IEventBus:
        return self._event_bus

    @event_bus.setter
    def event_bus(self, value: IEventBus) -> None:
        self._event_bus = value

    @property
    def tasks(self) -> ITaskManager:
        return self._tasks

    @tasks.setter
    def tasks(self, value: ITaskManager) -> None:
        self._tasks = value

    @property
    def modules(self) -> list[Any]:
        return self.extension_manager.registered_extensions

    @property
    def logger(self) -> ILogger:
        try:
            return self.container.resolve(ILogger)
        except Exception:
            from sagittarius_engine.utils.null_logger import NullLogger
            return NullLogger()

    @property
    def config(self) -> IConfig | None:
        try:
            return self.container.resolve(IConfig)
        except Exception:
            return None
``````

# FILE: kernel/dispatcher.py

```python
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext
import warnings
from sagittarius_engine.interfaces import ILogger
from sagittarius_engine.interfaces.i_dispatchable import IDispatchable

class Dispatcher:

def __init__(self, context: "IKernelContext") -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def dispatch(
        self,
        handler_class: type[IDispatchable],
        input_dto: object | None = None,
    ) -> Any:
        
        logger = self._get_logger()
        if logger:
            msg_type = "query" if "Query" in handler_class.__name__ else "command"
            logger.info(
                f"Executing {msg_type}: {handler_class.__name__}",
                extra={"submodule": "Dispatcher"},
            )
        handler = self.context.container.resolve(handler_class)

        def final() -> Any:
            return handler.execute(input_dto)

        return self.context.middleware_pipeline.execute(handler, input_dto, final)

    def execute(self, command_class: type, input_dto: object | None = None) -> Any:
        
        warnings.warn(
            "Dispatcher.execute is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: object | None = None) -> Any:
        
        warnings.warn(
            "Dispatcher.query is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)
``````

# FILE: kernel/events.py

```python
from dataclasses import dataclass

@dataclass
class ExtensionInitializing:

extension_name: str

@dataclass
class ExtensionStarted:

extension_name: str

@dataclass
class ExtensionStopped:

extension_name: str

@dataclass
class ExtensionDisposed:

extension_name: str
``````

# FILE: kernel/extension_manager.py

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext
    from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor
from sagittarius_engine.interfaces.i_module import IModule
from sagittarius_engine.kernel.events import (
    ExtensionInitializing,
    ExtensionStarted,
    ExtensionStopped,
    ExtensionDisposed,
)
from sagittarius_engine.exceptions import (
    ExtensionDependencyError,
    ExtensionCircularDependencyError,
)

class ModuleExtensionAdapter(IExtension):

def __init__(self, legacy_module: IModule):
        self.legacy_module = legacy_module
        deps = getattr(legacy_module, "dependencies", [])
        opt_deps = getattr(legacy_module, "optional_dependencies", [])
        prio = getattr(legacy_module, "priority", 0)
        enabled = getattr(legacy_module, "enabled", True)
        self._descriptor = ExtensionDescriptor(
            name=legacy_module.__class__.__name__,
            dependencies=deps if isinstance(deps, list) else [],
            optional_dependencies=opt_deps if isinstance(opt_deps, list) else [],
            priority=prio if isinstance(prio, int) else 0,
            enabled=enabled if isinstance(enabled, bool) else True,
        )

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._descriptor

    def register(self, context: "IEngineContext") -> None:
        from typing import cast

        kernel_ctx = cast("IKernelContext", context)
        self.legacy_module.register(kernel_ctx.app)

    def boot(self, context: "IEngineContext") -> None:
        from typing import cast

        kernel_ctx = cast("IKernelContext", context)
        self.legacy_module.boot(kernel_ctx.app)

    def shutdown(self, context: "IEngineContext") -> None:
        pass

    def __getattr__(self, name: str) -> object:
        return getattr(self.legacy_module, name)

def create_module_extension_adapter(legacy_module: IModule) -> ModuleExtensionAdapter:
    
    cls_name = legacy_module.__class__.__name__

    dynamic_cls = type(cls_name, (ModuleExtensionAdapter,), {})
    return dynamic_cls(legacy_module)

class ExtensionManager:

def __init__(self, context: "IKernelContext") -> None:
        self.context = context
        self.registered_extensions: list[IExtension] = []
        self.sorted_extensions: list[IExtension] = []
        self.initialized_extensions: list[IExtension] = []

    def register(self, extension_or_module: IExtension | IModule) -> None:
        
        if isinstance(extension_or_module, IExtension):
            ext = extension_or_module
        elif isinstance(extension_or_module, IModule):
            ext = create_module_extension_adapter(extension_or_module)
        else:
            raise TypeError(
                f"Cannot register '{type(extension_or_module).__name__}': "
                "object must implement IExtension or IModule. "
                "Wrap duck-typed objects in a ModuleExtensionAdapter manually."
            )

        self.registered_extensions.append(ext)

try:
            self._try_initialize_available()
        except (RuntimeError, ValueError, TypeError, ImportError) as e:
            self._rollback()
            raise e

    def _get_logger(self) -> "ILogger | None":
        try:
            return self.context.logger
        except AttributeError:
            return None

    def _emit(self, event_name: str, event_data: object) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except (RuntimeError, ValueError) as e:
            self.context.logger.error(f"Failed to emit event: {e}")

    def _try_initialize_available(self) -> None:
        
        initialized_names = {ext.descriptor.name for ext in self.initialized_extensions}
        enabled_exts = [
            ext for ext in self.registered_extensions if ext.descriptor.enabled
        ]

        while True:
            initialized_any = False

            sorted_exts = sorted(
                enabled_exts, key=lambda e: e.descriptor.priority, reverse=True
            )
            for ext in sorted_exts:
                name = ext.descriptor.name
                if name in initialized_names:
                    continue

deps_satisfied = True
                for dep in ext.descriptor.dependencies:
                    if dep not in initialized_names:
                        deps_satisfied = False
                        break

if deps_satisfied:
                    for dep in ext.descriptor.optional_dependencies:
                        if dep not in initialized_names:
                            deps_satisfied = False
                            break

                if deps_satisfied:
                    logger = self._get_logger()
                    if logger:
                        logger.info(f"Initializing extension '{name}'...")
                    self._emit("extension.initializing", ExtensionInitializing(name))
                    ext.initialize(self.context)
                    self.initialized_extensions.append(ext)
                    initialized_names.add(name)
                    initialized_any = True

            if not initialized_any:
                break

    def _build_and_sort(self) -> list[IExtension]:
        
        enabled_exts = [
            ext for ext in self.registered_extensions if ext.descriptor.enabled
        ]
        ext_by_name = {ext.descriptor.name: ext for ext in enabled_exts}

        visiting = set()
        visited = set()
        result = []

        def dfs(name: str):
            if name in visiting:
                raise ExtensionCircularDependencyError(
                    f"Circular dependency detected involving extension '{name}'"
                )
            if name in visited:
                return

            ext = ext_by_name.get(name)
            if not ext:
                return

            visiting.add(name)

for dep in ext.descriptor.dependencies:
                if dep not in ext_by_name:
                    raise ExtensionDependencyError(
                        f"Extension '{name}' requires missing dependency '{dep}'"
                    )
                dfs(dep)

for dep in ext.descriptor.optional_dependencies:
                if dep in ext_by_name:
                    dfs(dep)

            visiting.remove(name)
            visited.add(name)
            result.append(ext)

sorted_by_priority = sorted(
            enabled_exts, key=lambda e: e.descriptor.priority, reverse=True
        )
        for ext in sorted_by_priority:
            dfs(ext.descriptor.name)

        return result

    def initialize_and_start(self) -> None:
        
        logger = self._get_logger()
        self.sorted_extensions = self._build_and_sort()

for ext in self.sorted_extensions:
            if ext not in self.initialized_extensions:
                name = ext.descriptor.name
                if logger:
                    logger.info(f"Initializing extension '{name}'...")
                self._emit("extension.initializing", ExtensionInitializing(name))
                try:
                    ext.initialize(self.context)
                    self.initialized_extensions.append(ext)
                except (RuntimeError, ValueError, TypeError, ImportError) as e:
                    if logger:
                        logger.error(
                            f"Failed to initialize extension '{name}': {e}. Rolling back..."
                        )
                    self._rollback()
                    raise e

for ext in self.sorted_extensions:
            name = ext.descriptor.name
            if logger:
                logger.info(f"Starting extension '{name}'...")
            ext.start(self.context)
            self._emit("extension.started", ExtensionStarted(name))

            self._schedule_boot_async(ext)

    def _schedule_boot_async(self, ext: IExtension) -> None:
        
        try:
            async_runtime = getattr(self.context, "async_runtime", None)
            if async_runtime is None or not async_runtime.loop or not async_runtime.loop.is_running():
                return

            if type(ext).boot_async is IExtension.boot_async:
                return
            async_runtime.run_coroutine(ext.boot_async(self.context))
        except (RuntimeError, ValueError, TypeError) as e:
            logger = self._get_logger()
            if logger:
                logger.warning(f"[AsyncLifecycle] Could not schedule boot_async for '{ext.descriptor.name}': {e}")

    def _schedule_shutdown_async(self, ext: IExtension) -> None:
        
        try:
            async_runtime = getattr(self.context, "async_runtime", None)
            if async_runtime is None or not async_runtime.loop or not async_runtime.loop.is_running():
                return
            if type(ext).shutdown_async is IExtension.shutdown_async:
                return
            future = async_runtime.run_coroutine(ext.shutdown_async(self.context))
            future.result(timeout=10.0)
        except (RuntimeError, ValueError, TimeoutError) as e:
            logger = self._get_logger()
            if logger:
                logger.warning(f"[AsyncLifecycle] Could not run shutdown_async for '{ext.descriptor.name}': {e}")

    def _rollback(self) -> None:
        
        logger = self._get_logger()
        for ext in reversed(self.initialized_extensions):
            name = ext.descriptor.name
            if logger:
                logger.info(f"Disposing extension '{name}' due to rollback...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except (RuntimeError, ValueError, TypeError) as e:
                if logger:
                    logger.error(f"Error during rollback disposal of '{name}': {e}")

        self.initialized_extensions.clear()

    def stop_and_dispose(self) -> None:
        
        logger = self._get_logger()
        for ext in reversed(self.sorted_extensions):
            name = ext.descriptor.name

            self._schedule_shutdown_async(ext)
            if logger:
                logger.info(f"Stopping extension '{name}'...")
            try:
                ext.stop(self.context)
                self._emit("extension.stopped", ExtensionStopped(name))
            except (RuntimeError, ValueError, TypeError) as e:
                if logger:
                    logger.error(f"Error stopping extension '{name}': {e}")

            if logger:
                logger.info(f"Disposing extension '{name}'...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except (RuntimeError, ValueError, TypeError) as e:
                if logger:
                    logger.error(f"Error disposing extension '{name}': {e}")

        self.sorted_extensions.clear()
        self.initialized_extensions.clear()
``````

# FILE: kernel/i_kernel_context.py

```python
from abc import abstractmethod
from typing import TYPE_CHECKING
from sagittarius_engine.interfaces.i_engine_context import IEngineContext

if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App
    from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
    from sagittarius_engine.kernel.lifecycle import EngineLifecycle
    from sagittarius_engine.kernel.module_loader import ModuleLoader
    from sagittarius_engine.kernel.bootstrap import Bootstrap
    from sagittarius_engine.kernel.dispatcher import Dispatcher
    from sagittarius_engine.kernel.extension_manager import ExtensionManager
    from sagittarius_engine.runtime.async_runtime.async_runtime import AsyncRuntime
    from sagittarius_engine.runtime.scheduler.scheduler import Scheduler
    from sagittarius_engine.runtime.hosted.hosted_service_manager import (
        HostedServiceManager,
    )

class IKernelContext(IEngineContext):

app: "App"
    middleware_pipeline: "MiddlewarePipeline"
    lifecycle: "EngineLifecycle"
    module_loader: "ModuleLoader"
    bootstrap: "Bootstrap"
    dispatcher: "Dispatcher"
    extension_manager: "ExtensionManager"
    async_runtime: "AsyncRuntime"
    scheduler: "Scheduler"
    hosted_services: "HostedServiceManager"

    @property
    @abstractmethod
    def modules(self) -> list: ...
``````

# FILE: kernel/lifecycle.py

```python
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext

class Lifecycle:
    def __init__(self, context: "IKernelContext") -> None:
        self._state = "created"

class EngineState(Enum):
    STOPPED = "stopped"
    BOOTING = "booting"
    BOOTED = "booted"
    STOPPING = "stopping"

class EngineLifecycle:

def __init__(self, context: "IKernelContext") -> None:
        self.context = context
        self.state = EngineState.STOPPED

    def set_booting(self) -> None:
        self.state = EngineState.BOOTING

    def set_booted(self) -> None:
        self.state = EngineState.BOOTED

    def set_stopping(self) -> None:
        self.state = EngineState.STOPPING

    def set_stopped(self) -> None:
        self.state = EngineState.STOPPED

    @property
    def is_booted(self) -> bool:
        return self.state == EngineState.BOOTED

    @property
    def is_booting(self) -> bool:
        return self.state == EngineState.BOOTING

    @property
    def is_stopping(self) -> bool:
        return self.state == EngineState.STOPPING

    @property
    def is_stopped(self) -> bool:
        return self.state == EngineState.STOPPED
``````

# FILE: kernel/middleware_pipeline.py

```python
import functools
from collections.abc import Callable
from typing import TypeVar
from sagittarius_engine.interfaces import IMiddleware

TOutput = TypeVar("TOutput")

class MiddlewarePipeline:

def __init__(self) -> None:
        self.middlewares: list[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        
        self.middlewares.append(middleware)

    def execute(
        self,
        cmd_or_query: object,
        dto: object | None,
        final_handler: Callable[[], TOutput],
    ) -> TOutput:

next_handler = final_handler
        for middleware in reversed(self.middlewares):
            next_handler = functools.partial(
                middleware.process, cmd_or_query, dto, next_handler
            )
        return next_handler()
``````

# FILE: kernel/module_auto_discovery.py

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App

class ModuleAutoDiscovery:

@staticmethod
    def discover(modules_package_str_path: str, app: "App") -> None:
        
        from sagittarius_engine.kernel.module_loader import ModuleLoader

        loader = ModuleLoader(app)
        loader.discover_and_load(modules_package_str_path)
``````

# FILE: kernel/module_loader.py

```python
import importlib
import inspect
import pkgutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext
from sagittarius_engine.base.base_module import BaseModule
from sagittarius_engine.interfaces import IModule, ILogger

class ModuleLoader:

def __init__(self, context_or_app: "App | IKernelContext") -> None:
        self.context_or_app = context_or_app

    @property
    def context(self) -> "IKernelContext":
        if hasattr(self.context_or_app, "context"):
            return self.context_or_app.context
        return self.context_or_app

    def _get_logger(self) -> ILogger | None:
        try:
            return self.context.logger
        except Exception:
            try:
                return self.context.container.resolve(ILogger)
            except Exception:
                return None

    def discover_and_load(self, package_path: str) -> None:
        
        logger = self._get_logger()
        try:
            package = importlib.import_module(package_path)
        except ImportError as e:
            if logger:
                logger.warning(f"Could not discover package {package_path}: {e}")
            return

        if not hasattr(package, "__path__"):
            return

        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f"{package_path}.{name}"
            try:
                sub_package = importlib.import_module(full_module_name)
                for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                    if (
                        issubclass(obj, IModule)
                        and obj is not IModule
                        and obj is not BaseModule
                    ):
                        if hasattr(self.context, "app") and self.context.app:
                            self.context.app.use(obj())
                        elif hasattr(self.context_or_app, "use"):
                            self.context_or_app.use(obj())
            except Exception as e:
                if logger:
                    logger.error(f"Failed to load module {full_module_name}: {e}")
``````

# FILE: middleware/__init__.py

```python
from .logging_middleware import LoggingMiddleware
from .pydantic_validation_middleware import PydanticValidationMiddleware
from .timing_middleware import TimingMiddleware
from .transaction_middleware import TransactionMiddleware
from .validation_middleware import ValidationMiddleware

__all__ = [
    "LoggingMiddleware",
    "PydanticValidationMiddleware",
    "TimingMiddleware",
    "TransactionMiddleware",
    "ValidationMiddleware",
]
``````

# FILE: middleware/logging_middleware.py

```python
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IContainer, ILogger, IMiddleware

class LoggingMiddleware(IMiddleware):

def __init__(self, container: IContainer):
        
        self.container = container

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        name = cmd_or_query.__class__.__name__

        try:
            logger: ILogger = self.container.resolve(ILogger)
            logger.info(f"[LoggingMiddleware] Starting {name}")
        except Exception:
            logger = None
            print(f"[LoggingMiddleware] Starting {name}")

        result = next_handler()

        if logger:
            logger.info(f"[LoggingMiddleware] Finished {name}")
        else:
            print(f"[LoggingMiddleware] Finished {name}")

        return result
``````

# FILE: middleware/pydantic_validation_middleware.py

```python
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IMiddleware, IContainer

try:

    from pydantic import BaseModel, ValidationError
except ImportError:
    BaseModel = None
    ValidationError = None

class PydanticValidationMiddleware(IMiddleware):

def __init__(
        self, container: IContainer | None = None, model_class: Any = None
    ) -> None:
        
        if BaseModel is None:
            raise ImportError(
                "pydantic is not installed. Please install it using `pip install pydantic`."
            )
        self.container = container
        self.model_class = model_class

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        import typing
        model_class = self.model_class

        if model_class is None:

            try:
                type_hints = typing.get_type_hints(cmd_or_query.execute)
                for hint in type_hints.values():
                    if isinstance(hint, type) and issubclass(hint, BaseModel):
                        model_class = hint
                        break
            except Exception:
                pass

            if model_class is None:
                if isinstance(data_transfer_obj, BaseModel):
                    model_class = type(data_transfer_obj)
                else:
                    return next_handler()

        try:
            if hasattr(model_class, "model_validate"):

                if data_transfer_obj is None:
                    validated_dto = model_class()
                elif isinstance(data_transfer_obj, dict):
                    validated_dto = model_class.model_validate(data_transfer_obj)
                elif isinstance(data_transfer_obj, model_class):
                    validated_dto = data_transfer_obj
                else:
                    try:
                        validated_dto = model_class.model_validate(
                            data_transfer_obj
                        )
                    except Exception:
                        dto_dict = (
                            data_transfer_obj.__dict__
                            if hasattr(data_transfer_obj, "__dict__")
                            else {}
                        )
                        validated_dto = model_class.model_validate(dto_dict)
            else:

                if data_transfer_obj is None:
                    validated_dto = model_class()
                elif isinstance(data_transfer_obj, dict):
                    validated_dto = model_class(**data_transfer_obj)
                elif isinstance(data_transfer_obj, model_class):
                    validated_dto = data_transfer_obj
                else:
                    dto_dict = (
                        data_transfer_obj.__dict__
                        if hasattr(data_transfer_obj, "__dict__")
                        else {}
                    )
                    validated_dto = model_class(**dto_dict)
            data_transfer_obj = validated_dto
        except ValidationError as e:
            raise ValueError(
                f"Validation failed for {cmd_or_query.__class__.__name__}: {e}"
            )

        return next_handler()
``````

# FILE: middleware/timing_middleware.py

```python
import time
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IMiddleware

class TimingMiddleware(IMiddleware):

def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        start_time = time.time()
        result = next_handler()
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(
            f"[TimingMiddleware] {cmd_or_query.__class__.__name__} executed in {duration:.2f} ms"
        )
        return result
``````

# FILE: middleware/transaction_middleware.py

```python
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IContainer, IMiddleware
from sagittarius_engine.extensions.persistence import ISession

class TransactionMiddleware(IMiddleware):

def __init__(self, container: IContainer):
        self._container = container

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        session: ISession = self._container.resolve(ISession)
        try:
            result = next_handler()
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
``````

# FILE: middleware/validation_middleware.py

```python
import logging
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IMiddleware

logger = logging.getLogger(__name__)

class ValidationMiddleware(IMiddleware):

def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        logger.debug(
            f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}"
        )
        if data_transfer_obj is None:
            logger.warning("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
``````

# FILE: runtime/__init__.py

```python
from .hosted import IHostedService, HostedServiceManager, BackgroundService
from .tasks import CancellationToken, BackgroundTask, TaskManager
from .scheduler import Scheduler, ITrigger, IntervalTrigger, CronTrigger
from .async_runtime import AsyncRuntime

__all__ = [
    "IHostedService",
    "HostedServiceManager",
    "BackgroundService",
    "CancellationToken",
    "BackgroundTask",
    "TaskManager",
    "Scheduler",
    "ITrigger",
    "IntervalTrigger",
    "CronTrigger",
    "AsyncRuntime",
]
``````

# FILE: runtime/async_runtime/__init__.py

```python
from .async_runtime import AsyncRuntime

__all__ = ["AsyncRuntime"]
``````

# FILE: runtime/async_runtime/async_runtime.py

```python
import asyncio
import logging
import threading
from typing import Any, Coroutine

class AsyncRuntime:

def __init__(self, context: Any) -> None:
        self.context = context
        self.loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._logger = logging.getLogger("App")

    def start(self) -> None:
        
        if self._thread is not None:
            return

        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, name="AsyncRuntimeLoop", daemon=True
        )
        self._thread.start()
        self._logger.info("AsyncRuntime event loop started on background thread.")

    def _run_loop(self) -> None:
        if self.loop is not None:
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

    def run_coroutine(self, coro: Coroutine) -> Any:
        
        if self.loop is None or not self.loop.is_running():
            raise RuntimeError("AsyncRuntime loop is not running")
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def stop(self) -> None:
        
        if self.loop is None:
            return

        self._logger.info("Stopping AsyncRuntime event loop...")
        self.loop.call_soon_threadsafe(self.loop.stop)

        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

        try:
            pending = asyncio.all_tasks(self.loop)
            if pending:
                for task in pending:
                    task.cancel()
        except (RuntimeError, asyncio.InvalidStateError) as e:
            self._logger.warning(
                f"[AsyncRuntime] Error cancelling pending tasks during stop: {e}"
            )

        self.loop.close()
        self.loop = None
        self._logger.info("AsyncRuntime event loop stopped.")
``````

# FILE: runtime/hosted/__init__.py

```python
from .hosted_service import IHostedService
from .hosted_service_manager import HostedServiceManager
from .background_service import BackgroundService

__all__ = ["IHostedService", "HostedServiceManager", "BackgroundService"]
``````

# FILE: runtime/hosted/background_service.py

```python
from abc import abstractmethod
from typing import Optional
from sagittarius_engine.interfaces import IEngineContext, ITaskHandle
from sagittarius_engine.runtime.hosted.hosted_service import IHostedService
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken

class BackgroundService(IHostedService):

def __init__(self) -> None:
        self.token = CancellationToken()
        self.task: Optional[ITaskHandle] = None

    def start(self, context: IEngineContext) -> None:
        
        self.task = context.tasks.spawn(
            self._run_wrapper, name=self.__class__.__name__, token=self.token
        )

    def _run_wrapper(self, token: CancellationToken) -> None:
        self.run(token)

    @abstractmethod
    def run(self, token: CancellationToken) -> None:
        
        pass

    def stop(self, context: IEngineContext) -> None:
        
        self.token.cancel()

    def wait_for_exit(self) -> None:
        
        if self.task and self.task.future:
            try:
                self.task.future.result()
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Error in background service task: {e}")
``````

# FILE: runtime/hosted/events.py

```python
from dataclasses import dataclass

@dataclass
class HostedServiceStarted:

service_name: str

@dataclass
class HostedServiceStopped:

service_name: str
``````

# FILE: runtime/hosted/hosted_service_manager.py

```python
import logging
from typing import Any, List
from sagittarius_engine.runtime.hosted.hosted_service import IHostedService
from sagittarius_engine.runtime.hosted.events import (
    HostedServiceStarted,
    HostedServiceStopped,
)

class HostedServiceManager:

def __init__(self, context: Any) -> None:
        self.context = context
        self.services: List[IHostedService] = []
        self.started_services: List[IHostedService] = []
        self._logger = logging.getLogger("App")

    def register(self, service: IHostedService) -> None:
        
        if not isinstance(service, IHostedService):
            raise TypeError("Service must implement IHostedService")
        self.services.append(service)

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception as e:
            self.context.logger.error(f"Failed to emit event: {e}")

    def start(self) -> None:
        
        for service in self.services:
            name = service.__class__.__name__
            self._logger.info(f"Starting Hosted Service '{name}'...")
            try:
                service.start(self.context)
                self.started_services.append(service)
                self._emit("runtime.hosted.started", HostedServiceStarted(name))
            except Exception as e:
                self._logger.error(
                    f"Failed to start Hosted Service '{name}': {e}. Rolling back..."
                )
                self._rollback(e)
                raise e

    def _rollback(self, original_error: Exception) -> None:
        
        for service in reversed(self.started_services):
            name = service.__class__.__name__
            self._logger.info(f"Stopping Hosted Service '{name}' due to rollback...")
            try:
                service.stop(self.context)
                self._emit("runtime.hosted.stopped", HostedServiceStopped(name))
            except Exception as stop_error:
                self._logger.error(
                    f"Error stopping Hosted Service '{name}' during rollback: {stop_error}"
                )
        self.started_services.clear()

    def stop(self) -> None:
        
        errors = []
        for service in reversed(self.started_services):
            name = service.__class__.__name__
            self._logger.info(f"Stopping Hosted Service '{name}'...")
            try:
                service.stop(self.context)
                self._emit("runtime.hosted.stopped", HostedServiceStopped(name))
            except Exception as e:
                self._logger.error(f"Error stopping Hosted Service '{name}': {e}")
                errors.append(e)

        self.started_services.clear()
        if errors:
            raise RuntimeError(f"Multiple errors stopping hosted services: {errors}")
``````

# FILE: runtime/hosted/hosted_service.py

```python
from abc import ABC, abstractmethod
from sagittarius_engine.interfaces.i_engine_context import IEngineContext

class IHostedService(ABC):

@abstractmethod
    def start(self, context: IEngineContext) -> None:
        
        pass

    @abstractmethod
    def stop(self, context: IEngineContext) -> None:
        
        pass
``````

# FILE: runtime/scheduler/__init__.py

```python
from .scheduler import Scheduler
from .triggers import ITrigger, IntervalTrigger, CronTrigger

__all__ = ["Scheduler", "ITrigger", "IntervalTrigger", "CronTrigger"]
``````

# FILE: runtime/scheduler/events.py

```python
from dataclasses import dataclass

@dataclass
class SchedulerStarted:

@dataclass
class SchedulerStopped:
    
``````

# FILE: runtime/scheduler/scheduler.py

```python
import logging
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional
from sagittarius_engine.interfaces import IEngineContext
from sagittarius_engine.runtime.scheduler.triggers import (
    ITrigger,
    IntervalTrigger,
    CronTrigger,
)
from sagittarius_engine.runtime.scheduler.events import (
    SchedulerStarted,
    SchedulerStopped,
)

class ScheduledJob:

def __init__(
        self, fn: Callable, trigger: ITrigger, max_runs: Optional[int] = None
    ) -> None:
        self.fn = fn
        self.trigger = trigger
        self.max_runs = max_runs
        self.runs = 0
        self.next_run = trigger.get_next_run(datetime.now())

class JobBuilder:

def __init__(
        self,
        scheduler: "Scheduler",
        trigger: ITrigger,
        max_runs: Optional[int] = None,
    ) -> None:
        self.scheduler = scheduler
        self.trigger = trigger
        self.max_runs = max_runs

    def do(self, fn: Callable) -> ScheduledJob:
        
        job = ScheduledJob(fn, self.trigger, self.max_runs)
        self.scheduler.add_job(job)
        return job

class Scheduler:

def __init__(self, context: IEngineContext) -> None:
        self.context = context
        self.jobs: List[ScheduledJob] = []
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._running = False
        self._thread: threading.Thread | None = None
        self._logger = logging.getLogger("App")

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception as e:
            self.context.logger.error(f"Failed to emit event: {e}")

    def start(self) -> None:
        
        with self._lock:
            if self._running:
                return
            self._running = True

        self._thread = threading.Thread(
            target=self._run, name="SagittariusScheduler", daemon=True
        )
        self._thread.start()
        self._logger.info("Scheduler started.")
        self._emit("runtime.scheduler.started", SchedulerStarted())

    def stop(self) -> None:
        
        with self._lock:
            if not self._running:
                return
            self._running = False
            self._cond.notify_all()

        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None
        self._logger.info("Scheduler stopped.")
        self._emit("runtime.scheduler.stopped", SchedulerStopped())

    def add_job(self, job: ScheduledJob) -> None:
        
        with self._lock:
            self.jobs.append(job)
            self._cond.notify_all()

    def every(
        self, seconds: float = 0, minutes: float = 0, hours: float = 0
    ) -> JobBuilder:
        
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours)
        return JobBuilder(self, IntervalTrigger(delta))

    def after(
        self, seconds: float = 0, minutes: float = 0, hours: float = 0
    ) -> JobBuilder:
        
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours)
        return JobBuilder(self, IntervalTrigger(delta), max_runs=1)

    def cron(self, cron_expr: str) -> JobBuilder:
        
        return JobBuilder(self, CronTrigger(cron_expr))

    def _run(self) -> None:
        while True:
            with self._lock:
                if not self._running:
                    break

                now = datetime.now()
                jobs_to_run = []
                active_jobs = []
                next_wakeup = now + timedelta(seconds=1.0)

                for job in self.jobs:
                    if job.next_run <= now:
                        jobs_to_run.append(job)
                    else:
                        active_jobs.append(job)
                        if job.next_run < next_wakeup:
                            next_wakeup = job.next_run
                self.jobs = active_jobs

for job in jobs_to_run:
                    try:
                        self.context.tasks.spawn(
                            job.fn, name=f"ScheduledJob_{job.fn.__name__}"
                        )
                    except Exception as e:
                        self._logger.error(f"Failed to spawn scheduled job: {e}")

                    job.runs += 1
                    if job.max_runs is None or job.runs < job.max_runs:
                        job.next_run = job.trigger.get_next_run(now)
                        self.jobs.append(job)
                        if job.next_run < next_wakeup:
                            next_wakeup = job.next_run

sleep_time = (next_wakeup - datetime.now()).total_seconds()
                if sleep_time <= 0:
                    sleep_time = 0.01

self._cond.wait(sleep_time)
``````

# FILE: runtime/scheduler/triggers.py

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class ITrigger(ABC):

@abstractmethod
    def get_next_run(self, from_time: datetime) -> datetime:
        
        pass

class IntervalTrigger(ITrigger):

def __init__(self, delta: timedelta) -> None:
        self.delta = delta

    def get_next_run(self, from_time: datetime) -> datetime:
        return from_time + self.delta

class CronTrigger(ITrigger):

def __init__(self, cron_expr: str) -> None:
        self.cron_expr = cron_expr

    def get_next_run(self, from_time: datetime) -> datetime:

        next_min = from_time.replace(second=0, microsecond=0) + timedelta(minutes=1)
        return next_min
``````

# FILE: runtime/tasks/__init__.py

```python
from .cancellation_token import CancellationToken
from .background_task import BackgroundTask
from .task_manager import TaskManager

__all__ = ["CancellationToken", "BackgroundTask", "TaskManager"]
``````

# FILE: runtime/tasks/background_task.py

```python
from enum import Enum
import uuid
from typing import Any, Optional, Callable
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
from datetime import datetime, timezone

from sagittarius_engine.interfaces.i_task_manager import ITaskHandle

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class BackgroundTask(ITaskHandle):

def __init__(
        self,
        name: str,
        token: Optional[CancellationToken] = None,
        critical: bool = False,
        on_progress_update: Optional[Callable[[float, str], None]] = None,
    ) -> None:
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self.critical: bool = critical
        self._token: CancellationToken = (
            token if token is not None else CancellationToken()
        )
        self._future: Optional[Any] = None
        self._status: TaskState = TaskState.PENDING
        self._progress: float = 0.0
        self._on_progress_update: Optional[Callable[[float, str], None]] = (
            on_progress_update
        )
        self.error: Optional[Exception] = None
        self.start_time: Optional[datetime] = datetime.now(timezone.utc)
        self.end_time: Optional[datetime] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def token(self) -> CancellationToken:
        return self._token

    @token.setter
    def token(self, value: CancellationToken) -> None:
        self._token = value

    @property
    def future(self) -> Optional[Any]:
        return self._future

    @future.setter
    def future(self, value: Optional[Any]) -> None:
        self._future = value

    @property
    def status(self) -> TaskState:
        return self._status

    @status.setter
    def status(self, value: TaskState) -> None:
        self._status = value
        if value in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED):
            self.end_time = datetime.now(timezone.utc)

    @property
    def progress(self) -> float:
        return self._progress

    def update_progress(self, value: float, message: str = "") -> None:
        
        if not (0.0 <= value <= 100.0):
            raise ValueError("Progress must be between 0.0 and 100.0")
        self._progress = value
        if self._on_progress_update:
            self._on_progress_update(value, message)

    def cancel(self) -> None:
        
        self.token.cancel()
        if self.future is not None:
            self.future.cancel()
            self.status = TaskState.CANCELLED
``````

# FILE: runtime/tasks/cancellation_token.py

```python
import threading

class CancellationToken:

def __init__(self, event: threading.Event | None = None) -> None:
        self._event = event if event is not None else threading.Event()

    def is_cancelled(self) -> bool:
        
        return self._event.is_set()

    @property
    def is_cancellation_requested(self) -> bool:
        
        return self._event.is_set()

    def cancel(self) -> None:
        
        self._event.set()

    def wait(self, timeout: float | None = None) -> bool:
        
        return self._event.wait(timeout)
``````

# FILE: runtime/tasks/events.py

```python
from dataclasses import dataclass

@dataclass
class TaskStarted:

event_name = "runtime.tasks.started"
    task_id: str
    task_name: str

@dataclass
class TaskCompleted:

event_name = "runtime.tasks.completed"
    task_id: str
    task_name: str

@dataclass
class TaskProgressUpdated:

event_name = "runtime.tasks.progress"
    task_id: str
    progress: float
    message: str

@dataclass
class TaskFailed:

event_name = "runtime.tasks.failed"
    task_id: str
    task_name: str
    error: Exception
``````

# FILE: runtime/tasks/task_manager.py

```python
import inspect
import logging
import threading
import weakref
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional, Union
from sagittarius_engine.interfaces.i_task_manager import ITaskManager
from sagittarius_engine.runtime.tasks.background_task import BackgroundTask
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
from sagittarius_engine.runtime.tasks.events import (
    TaskStarted,
    TaskCompleted,
    TaskFailed,
    TaskProgressUpdated,
)
from sagittarius_engine.runtime.tasks.background_task import TaskState

class DaemonThreadPoolExecutor(ThreadPoolExecutor):

def _adjust_thread_count(self) -> None:
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = (
                f"{self._thread_name_prefix or 'ThreadPoolExecutor'}_{num_threads}"
            )
            try:
                import concurrent.futures.thread

                def weakref_cb(_, q=self._work_queue):
                    pass

                if hasattr(self, "_create_worker_context"):
                    t = threading.Thread(
                        name=thread_name,
                        target=concurrent.futures.thread._worker,
                        args=(
                            weakref.ref(self, weakref_cb),
                            self._create_worker_context(),
                            self._work_queue,
                        ),
                    )
                elif hasattr(self, "_initializer") and hasattr(self, "_initargs"):
                    t = threading.Thread(
                        name=thread_name,
                        target=concurrent.futures.thread._worker,
                        args=(
                            weakref.ref(self, weakref_cb),
                            self._work_queue,
                            self._initializer,
                            self._initargs,
                        ),
                    )
                else:
                    t = threading.Thread(
                        name=thread_name,
                        target=concurrent.futures.thread._worker,
                        args=(weakref.ref(self, weakref_cb), self._work_queue),
                    )
                t.daemon = True
                t.start()
                self._threads.add(t)
                concurrent.futures.thread._threads_queues[t] = self._work_queue
            except Exception:
                super()._adjust_thread_count()

class TaskManager(ITaskManager):

def __init__(self, context: Any) -> None:
        self.context = context
        self.tasks: Dict[str, BackgroundTask] = {}
        self.background_executor = DaemonThreadPoolExecutor(
            max_workers=20,
            thread_name_prefix="SagittariusBgTask",
        )
        self.critical_executor = ThreadPoolExecutor(
            max_workers=10,
            thread_name_prefix="SagittariusCriticalTask",
        )

        self.executor = self.background_executor
        self._lock = threading.Lock()
        self._logger = logging.getLogger("App")

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception as e:
            self.context.logger.error(f"Failed to emit event: {e}")

    def _cleanup_old_tasks(self) -> None:
        with self._lock:

            if len(self.tasks) > 200:
                finished_ids = [
                    tid
                    for tid, t in self.tasks.items()
                    if t.status
                    in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED)
                ]

                for tid in finished_ids[:-50]:
                    del self.tasks[tid]

    def _wrap_sync(
        self, bg_task: BackgroundTask, fn: Callable[[], Any]
    ) -> Callable[[], Any]:
        def wrapper():
            try:
                res = fn()
                bg_task.status = TaskState.COMPLETED
                self._emit(
                    "runtime.tasks.completed",
                    TaskCompleted(bg_task.id, bg_task.name),
                )
                return res
            except Exception as e:
                bg_task.status = TaskState.FAILED
                bg_task.error = e
                self._logger.error(f"Task '{bg_task.name}' failed: {e}")
                self._emit(
                    "runtime.tasks.failed",
                    TaskFailed(bg_task.id, bg_task.name, e),
                )
                raise e
            finally:
                self._cleanup_old_tasks()

        return wrapper

    async def _wrap_coro(self, bg_task: BackgroundTask, coro: Any) -> Any:
        try:
            res = await coro
            bg_task.status = TaskState.COMPLETED
            self._emit(
                "runtime.tasks.completed", TaskCompleted(bg_task.id, bg_task.name)
            )
            return res
        except Exception as e:
            bg_task.status = TaskState.FAILED
            bg_task.error = e
            self._logger.error(f"Async task '{bg_task.name}' failed: {e}")
            self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, bg_task.name, e))
            raise e
        finally:
            self._cleanup_old_tasks()

    def spawn(
        self,
        callable_or_coro: Union[Callable[..., Any], Any],
        name: Optional[str] = None,
        token: Optional[CancellationToken] = None,
        critical: bool = False,
    ) -> BackgroundTask:
        
        task_name = name or (
            callable_or_coro.__name__
            if hasattr(callable_or_coro, "__name__")
            else "UnnamedTask"
        )

        def _on_progress(val: float, msg: str):
            self._emit(
                "runtime.tasks.progress", TaskProgressUpdated(bg_task.id, val, msg)
            )

        bg_task = BackgroundTask(
            task_name, token, critical=critical, on_progress_update=_on_progress
        )

        with self._lock:
            self.tasks[bg_task.id] = bg_task

        self._emit("runtime.tasks.started", TaskStarted(bg_task.id, task_name))

if inspect.iscoroutinefunction(callable_or_coro) or inspect.iscoroutine(
            callable_or_coro
        ):

            coro = (
                callable_or_coro
                if inspect.iscoroutine(callable_or_coro)
                else callable_or_coro(bg_task.token)
            )
            bg_task.status = TaskState.RUNNING
            try:
                future = self.context.async_runtime.run_coroutine(
                    self._wrap_coro(bg_task, coro)
                )
                bg_task.future = future
            except Exception as e:
                bg_task.status = TaskState.FAILED
                bg_task.error = e
                self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e))
                raise e
        else:

            bg_task.status = TaskState.RUNNING
            try:
                sig = inspect.signature(callable_or_coro)
                if "token" in sig.parameters:

                    def fn():
                        return callable_or_coro(token=bg_task.token)
                else:

                    def fn():
                        return callable_or_coro()

                target_executor = (
                    self.critical_executor if critical else self.background_executor
                )
                future = target_executor.submit(self._wrap_sync(bg_task, fn))
                bg_task.future = future
            except Exception as e:
                bg_task.status = TaskState.FAILED
                bg_task.error = e
                self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e))
                raise e

        return bg_task

    def cancel_all(self) -> None:
        
        with self._lock:
            for task in self.tasks.values():
                if task.status == TaskState.RUNNING:
                    task.cancel()

    def shutdown(self, timeout: float = 5.0) -> None:
        
        self.cancel_all()

        with self._lock:
            critical_futures = [
                t.future
                for t in self.tasks.values()
                if t.critical and t.status == TaskState.RUNNING and t.future is not None
            ]

        if critical_futures:
            from concurrent.futures import wait

            wait(critical_futures, timeout=timeout)

        try:
            self.critical_executor.shutdown(wait=False, cancel_futures=True)
            self.background_executor.shutdown(wait=False, cancel_futures=True)
        except TypeError:
            self.critical_executor.shutdown(wait=False)
            self.background_executor.shutdown(wait=False)
``````

# FILE: sdk/__init__.py

```python
from .template_loader import TemplateLoader
from .template_renderer import TemplateRenderer
from .project_generator import ProjectGenerator

__all__ = ["TemplateLoader", "TemplateRenderer", "ProjectGenerator"]
``````

# FILE: sdk/cli.py

```python
import sys
import argparse
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.sdk.template_renderer import TemplateRenderer
from sagittarius_engine.sdk.project_generator import ProjectGenerator

def main():
    parser = argparse.ArgumentParser(description="Sagittarius CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

new_parser = subparsers.add_parser(
        "new", help="Create a new project from a template"
    )
    new_parser.add_argument(
        "template", help="Template name (e.g. minimal, clean, ddd, mvc)"
    )
    new_parser.add_argument("project_name", help="Name of the project to create")
    new_parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to create the project in (default: .)",
    )

    args = parser.parse_args()

    if args.command == "new":
        loader = TemplateLoader()
        renderer = TemplateRenderer()
        generator = ProjectGenerator(loader, renderer)

        available_templates = loader.list_templates()
        if args.template not in available_templates:
            print(
                f"Error: Template '{args.template}' not found. Available templates: {', '.join(available_templates)}"
            )
            sys.exit(1)

        try:
            project_path = generator.generate(
                project_name=args.project_name,
                template_name=args.template,
                output_dir=args.output_dir,
            )
            print(
                f"Project '{args.project_name}' created successfully from template '{args.template}' at '{project_path}'."
            )
        except Exception as e:
            print(f"Error generating project: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
``````

# FILE: sdk/project_generator.py

```python
import os
import shutil
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.sdk.template_renderer import TemplateRenderer

class ProjectGenerator:

def __init__(self, loader: TemplateLoader, renderer: TemplateRenderer) -> None:
        self.loader = loader
        self.renderer = renderer

    def generate(
        self,
        project_name: str,
        template_name: str,
        output_dir: str,
        extra_placeholders: dict[str, str] | None = None,
    ) -> str:
        
        template_path = self.loader.get_template_path(template_name)
        project_path = os.path.join(output_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        placeholders = {
            "project_name": project_name,
            "package_name": project_name.lower().replace("-", "_"),
            "author": "Developer",
            "python_version": "3.13",
        }
        if extra_placeholders:
            placeholders.update(extra_placeholders)

        for root, dirs, files in os.walk(template_path):
            relative_dir = os.path.relpath(root, template_path)
            if relative_dir == ".":
                dest_dir = project_path
            else:
                rendered_rel_dir = self.renderer.render(relative_dir, placeholders)
                dest_dir = os.path.join(project_path, rendered_rel_dir)
            os.makedirs(dest_dir, exist_ok=True)

            for file in files:
                src_file_path = os.path.join(root, file)
                rendered_file_name = self.renderer.render(file, placeholders)
                dest_file_path = os.path.join(dest_dir, rendered_file_name)

                try:
                    with open(src_file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    rendered_content = self.renderer.render(file_content, placeholders)
                    with open(dest_file_path, "w", encoding="utf-8") as f:
                        f.write(rendered_content)
                except UnicodeDecodeError:

                    shutil.copy2(src_file_path, dest_file_path)

        return project_path
``````

# FILE: sdk/template_loader.py

```python
import os
from typing import List

from sagittarius_engine.exceptions import PathTraversalError

class TemplateLoader:

def __init__(self) -> None:
        self.template_directories: List[str] = [
            os.path.join(os.path.dirname(__file__), "templates")
        ]

    def register_template_directory(self, path: str) -> None:
        
        if os.path.exists(path) and os.path.isdir(path):
            self.template_directories.append(path)

    def list_templates(self) -> List[str]:
        
        templates = set()
        for directory in self.template_directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for name in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, name)):
                        templates.add(name)
        return sorted(list(templates))

    def get_template_path(self, template_name: str) -> str:
        
        for directory in self.template_directories:
            path = os.path.join(directory, template_name)
            directory_real = os.path.realpath(directory)
            path_real = os.path.realpath(path)

            if os.path.commonpath([directory_real, path_real]) != directory_real:
                raise PathTraversalError(f"Path traversal detected: {template_name}")

            if os.path.exists(path) and os.path.isdir(path):
                return path
        raise ValueError(f"Template '{template_name}' not found.")
``````

# FILE: sdk/template_renderer.py

```python
import re

class TemplateRenderer:

_pattern = re.compile(r"\{\{\s*(.*?)\s*\}\}")

    def render(self, content: str, placeholders: dict[str, str]) -> str:

def replacer(match):
            key = match.group(1)
            if key in placeholders:
                return str(placeholders[key])
            return match.group(0)

        return self._pattern.sub(replacer, content)
``````

# FILE: sdk/templates/clean/adapters/__init__.py

```python

``````

# FILE: sdk/templates/clean/application/__init__.py

```python

``````

# FILE: sdk/templates/clean/domain/__init__.py

```python

``````

# FILE: sdk/templates/clean/infrastructure/__init__.py

```python

``````

# FILE: sdk/templates/clean/main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot(auto_discover="modules")
    print(
        "Clean Architecture App '{{project_name}}' booted successfully by {{author}}!"
    )

if __name__ == "__main__":
    main()
``````

# FILE: sdk/templates/clean/modules/__init__.py

```python

``````

# FILE: sdk/templates/ddd/application/__init__.py

```python

``````

# FILE: sdk/templates/ddd/domain/model/__init__.py

```python

``````

# FILE: sdk/templates/ddd/domain/services/__init__.py

```python

``````

# FILE: sdk/templates/ddd/infrastructure/__init__.py

```python

``````

# FILE: sdk/templates/ddd/interfaces/__init__.py

```python

``````

# FILE: sdk/templates/ddd/main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("DDD App '{{project_name}}' booted successfully by {{author}}!")

if __name__ == "__main__":
    main()
``````

# FILE: sdk/templates/minimal/main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("Minimal App '{{project_name}}' booted successfully by {{author}}!")

if __name__ == "__main__":
    main()
``````

# FILE: sdk/templates/mvc/controllers/__init__.py

```python

``````

# FILE: sdk/templates/mvc/main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("MVC App '{{project_name}}' booted successfully by {{author}}!")

if __name__ == "__main__":
    main()
``````

# FILE: sdk/templates/mvc/models/__init__.py

```python

``````

# FILE: sdk/templates/mvc/views/__init__.py

```python

``````

# FILE: utils/__init__.py

```python
from .path_utils import PathUtils

__all__ = ["PathUtils"]
``````

# FILE: utils/null_logger.py

```python
from typing import Any
from sagittarius_engine.interfaces.i_logger import ILogger

class NullLogger(ILogger):

def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass
``````

# FILE: utils/path_utils.py

```python
import os

class PathUtils:

@staticmethod
    def get_relative_path(base_file: str, *paths: str) -> str:
        
        return os.path.join(os.path.dirname(os.path.abspath(base_file)), *paths)
``````

