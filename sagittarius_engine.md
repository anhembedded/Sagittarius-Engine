# PROJECT CONTEXT

**Root:** `C:\Users\hoang\Documents\Sagittarius_ForkBoy\sagittarius_engine\`
**Pattern:** `*.py`
**Files:** 133
**Generated:** 2026-07-09 23:29:57

## Directory Tree

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
│   ├── base_output_port.py
│   └── base_repository.py
├── domain
│   ├── __init__.py
│   ├── base_event.py
│   └── i_domain_event.py
├── exceptions.py
├── extensions
│   ├── __init__.py
│   ├── cqrs
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   └── queries.py
│   ├── health_check_query.py
│   ├── health_module.py
│   ├── logger_module.py
│   ├── persistence
│   │   ├── __init__.py
│   │   ├── database_module.py
│   │   ├── i_session.py
│   │   ├── repository.py
│   │   └── sqlalchemy_session_adapter.py
│   └── thread_manager_module.py
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
│   │   └── std_logger.py
│   ├── persistence
│   │   ├── __init__.py
│   │   ├── database_module.py
│   │   ├── i_session.py
│   │   ├── i_thread_manager.py
│   │   └── sqlalchemy_session_adapter.py
│   ├── ports
│   │   ├── __init__.py
│   │   ├── i_file_storage.py
│   │   └── i_metrics.py
│   ├── storage
│   │   ├── __init__.py
│   │   ├── azure_blob_storage.py
│   │   ├── local_file_storage.py
│   │   └── s3_file_storage.py
│   └── thread_manager.py
├── interfaces
│   ├── __init__.py
│   ├── events.py
│   ├── i_async_event_bus.py
│   ├── i_command.py
│   ├── i_config.py
│   ├── i_container.py
│   ├── i_event_bus.py
│   ├── i_extension.py
│   ├── i_input_port.py
│   ├── i_logger.py
│   ├── i_middleware.py
│   ├── i_module.py
│   ├── i_output_port.py
│   └── i_query.py
├── kernel
│   ├── __init__.py
│   ├── app_runner.py
│   ├── app.py
│   ├── bootstrap.py
│   ├── context.py
│   ├── dispatcher.py
│   ├── extension_manager.py
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
│   │   ├── hosted_service_manager.py
│   │   └── hosted_service.py
│   ├── scheduler
│   │   ├── __init__.py
│   │   ├── scheduler.py
│   │   └── triggers.py
│   └── tasks
│       ├── __init__.py
│       ├── background_task.py
│       ├── cancellation_token.py
│       └── task_manager.py
├── sdk
│   ├── __init__.py
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
└── tools
    ├── __init__.py
    └── scaffold.py
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

# FILE: adapters\batch\__init__.py

```python
from .batch_input_port import BatchInputPort
from .batch_output_port import BatchOutputPort
from .const import FILE_TYPE_CSV, FILE_TYPE_JSON

__all__ = ["BatchInputPort", "BatchOutputPort", "FILE_TYPE_CSV", "FILE_TYPE_JSON"]
``````

# FILE: adapters\batch\batch_input_port.py

```python
import csv
import json
import os
from typing import Any, Iterator, Optional
from sagittarius_engine.kernel.app_runner import COMMAND_KEY, EXIT_COMMAND
from sagittarius_engine.base.base_input_port import BaseInputPort
from sagittarius_engine.adapters.batch.const import FILE_TYPE_CSV, FILE_TYPE_JSON

class BatchInputPort(BaseInputPort):

def __init__(self, file_path: str, file_type: str=FILE_TYPE_CSV) -> None:
        super().__init__()
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
                self.logger.error(f'File not found: {self.file_path}')
            self._iterator = iter([])
            return
        try:
            if self.file_type == FILE_TYPE_CSV:
                with open(self.file_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    self._iterator = iter(data)
            elif self.file_type == FILE_TYPE_JSON:
                with open(self.file_path, encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._iterator = iter(data)
                    else:
                        if self.logger:
                            self.logger.error('JSON file must contain an array of objects')
                        self._iterator = iter([])
            else:
                if self.logger:
                    self.logger.error(f'Unsupported file type: {self.file_type}')
                self._iterator = iter([])
        except Exception as e:
            if self.logger:
                self.logger.error(f'Error reading file {self.file_path}: {e}')
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

# FILE: adapters\batch\batch_output_port.py

```python
import json
import os
from typing import Any
from sagittarius_engine.base.base_output_port import BaseOutputPort

class BatchOutputPort(BaseOutputPort):

def __init__(self, output_path: str) -> None:
        super().__init__()
        self.output_path = output_path
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    def present(self, result: Any) -> None:
        
        try:
            with open(self.output_path, 'a', encoding='utf-8') as f:
                if isinstance(result, dict):
                    f.write(json.dumps(result) + '\n')
                else:
                    f.write(str(result) + '\n')
        except Exception as e:
            if self.logger:
                self.logger.error(f'Error writing to output file: {e}')

    def present_error(self, error: Exception) -> None:
        
        try:
            with open(self.output_path, 'a', encoding='utf-8') as f:
                f.write(f'ERROR: {error}\n')
        except Exception as e:
            if self.logger:
                self.logger.error(f'Error writing to output file: {e}')
``````

# FILE: adapters\batch\const.py

```python
FILE_TYPE_CSV = "csv"
FILE_TYPE_JSON = "json"
EXIT_COMMAND = "exit"
``````

# FILE: adapters\cli\__init__.py

```python
from .cli_input_port import CLIInputPort
from .cli_output_port import CLIOutputPort
from .const import COMMAND_KEY

__all__ = ["CLIInputPort", "CLIOutputPort", "COMMAND_KEY"]
``````

# FILE: adapters\cli\cli_input_port.py

```python
import argparse
import sys
from typing import Any
from sagittarius_engine.base.base_input_port import BaseInputPort
from sagittarius_engine.adapters.cli.const import COMMAND_KEY

class CLIInputPort(BaseInputPort):

def receive(self) -> dict[str, Any]:
        
        parser = argparse.ArgumentParser(description='CLI Input Port')
        parser.add_argument(COMMAND_KEY, type=str, help='The command to execute')
        args, unknown = parser.parse_known_args()
        result = {COMMAND_KEY: getattr(args, COMMAND_KEY)}
        i = 0
        while i < len(unknown):
            arg = unknown[i]
            if arg.startswith('--'):
                key = arg[2:]
                value = None
                if i + 1 < len(unknown) and (not unknown[i + 1].startswith('--')):
                    value = unknown[i + 1]
                    i += 1
                result[key] = value
            else:
                sys.exit(f'error: unrecognized arguments: {arg}')
            i += 1
        return result
``````

# FILE: adapters\cli\cli_output_port.py

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
        
        print(f'ERROR: {error}', file=sys.stderr)
``````

# FILE: adapters\cli\const.py

```python
COMMAND_KEY = "command"
EXIT_COMMAND = "exit"
``````

# FILE: base\__init__.py

```python
from .base_module import BaseModule
from .base_repository import BaseRepository
from .base_input_port import BaseInputPort
from .base_output_port import BaseOutputPort

__all__ = [
    "BaseModule",
    "BaseRepository",
    "BaseInputPort",
    "BaseOutputPort",
]
``````

# FILE: base\base_input_port.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces.i_input_port import IInputPort
from sagittarius_engine.interfaces.i_logger import ILogger

class BaseInputPort(IInputPort):

def __init__(self, logger: Optional[ILogger]=None) -> None:
        self.logger = logger

    def receive(self) -> dict[str, Any]:
        
        raise NotImplementedError('Subclasses must implement receive()')
``````

# FILE: base\base_module.py

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

# FILE: base\base_output_port.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_output_port import IOutputPort

class BaseOutputPort(IOutputPort):

def __init__(self, logger: Optional[ILogger]=None) -> None:
        self.logger = logger

    def present(self, result: Any) -> None:
        
        if self.logger:
            self.logger.info(f'Result: {result}')
        else:
            print(result)

    def present_error(self, error: Exception) -> None:
        
        if self.logger:
            self.logger.error(f'Error: {error}')
        else:
            print(f'Error: {error}')
``````

# FILE: base\base_repository.py

```python
import warnings
from sagittarius_engine.extensions.persistence.repository import BaseRepository

warnings.warn(
    "Importing BaseRepository from sagittarius_engine.base is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: domain\__init__.py

```python
from .i_domain_event import IDomainEvent
from .base_event import BaseEvent

__all__ = [
    "IDomainEvent",
    "BaseEvent",
]
``````

# FILE: domain\base_event.py

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

# FILE: domain\i_domain_event.py

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

# FILE: extensions\__init__.py

```python

``````

# FILE: extensions\cqrs\__init__.py

```python
from .commands import ICommand
from .queries import IQuery

__all__ = ["ICommand", "IQuery"]
``````

# FILE: extensions\cqrs\commands.py

```python
from abc import ABC, abstractmethod
from typing import Any

class ICommand(ABC):

@abstractmethod
    def execute(self, input_dto: Any) -> Any:
        
        ...
``````

# FILE: extensions\cqrs\queries.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IQuery(ABC):

@abstractmethod
    def execute(self, input_dto: Any) -> Any:
        
        ...
``````

# FILE: extensions\health_check_query.py

```python
from dataclasses import dataclass
from typing import Any
from sagittarius_engine.interfaces import IContainer, IEventBus, IQuery
from sagittarius_engine.infrastructure.persistence.i_session import ISession

@dataclass
class HealthCheckDTO:
    
    pass

class HealthCheckQuery(IQuery):

def __init__(self, container: IContainer, event_bus: IEventBus):
        self.container = container
        self.event_bus = event_bus

    def execute(self, input_dto: HealthCheckDTO | None=None) -> dict[str, Any]:
        
        status: dict[str, Any] = {'status': 'healthy', 'components': {'container': 'ok', 'event_bus': 'ok', 'database': 'unknown'}}
        try:
            self.container.resolve(IContainer)
        except Exception:
            status['components']['container'] = 'error: container resolution failed'
            status['status'] = 'unhealthy'
        try:
            if not hasattr(self.event_bus, 'emit'):
                raise ValueError('event_bus has no emit method')
        except Exception:
            status['components']['event_bus'] = 'error: event bus check failed'
            status['status'] = 'unhealthy'
        try:
            session: ISession = self.container.resolve(ISession)
            try:
                from sqlalchemy import text
                session.execute(text('SELECT 1'))
                status['components']['database'] = 'ok'
            except ImportError:
                status['components']['database'] = 'sqlalchemy not installed'
                status['status'] = 'unhealthy'
            except Exception as e:
                status['components']['database'] = 'database connection failed'
                status['status'] = 'unhealthy'
        except Exception:
            status['components']['database'] = 'not configured or resolving failed'
        return status
``````

# FILE: extensions\health_module.py

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.extensions.health_check_query import HealthCheckQuery

class HealthExtension(IExtension):

def register(self, context: "EngineContext") -> None:
        
        context.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, context: "EngineContext") -> None:
        
        pass

    def shutdown(self, context: "EngineContext") -> None:
        
        pass

class HealthModule(HealthExtension):

def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "HealthModule is deprecated. Use HealthExtension instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
``````

# FILE: extensions\logger_module.py

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.interfaces import IConfig, ILogger

class LoggerExtension(IExtension):

def register(self, context: "EngineContext") -> None:
        try:
            config: IConfig = context.container.resolve(IConfig)
        except Exception:
            config = None

        logger_instance = StdLogger(config)
        context.container.singleton(ILogger, logger_instance)

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass

class LoggerModule(LoggerExtension):

def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "LoggerModule is deprecated. Use LoggerExtension instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
``````

# FILE: extensions\persistence\__init__.py

```python
from .repository import BaseRepository
from .i_session import ISession
from .sqlalchemy_session_adapter import SQLAlchemySessionAdapter
from .database_module import DatabaseExtension, DatabaseModule, SqlAlchemyExtension

__all__ = [
    "BaseRepository",
    "ISession",
    "SQLAlchemySessionAdapter",
    "DatabaseExtension",
    "DatabaseModule",
    "SqlAlchemyExtension",
]
``````

# FILE: extensions\persistence\database_module.py

```python
from typing import TYPE_CHECKING, Any
import os

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

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

def register(self, context: "EngineContext") -> None:
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

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass

    def _get_logger(self, context: "EngineContext") -> ILogger | None:
        try:
            return context.container.resolve(ILogger)
        except Exception:
            return None

class DatabaseModule(DatabaseExtension):

def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "DatabaseModule is deprecated. Use DatabaseExtension (or SqlAlchemyExtension) instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)

SqlAlchemyExtension = DatabaseExtension
``````

# FILE: extensions\persistence\i_session.py

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

# FILE: extensions\persistence\repository.py

```python
from typing import Any, TypeVar
from sagittarius_engine.extensions.persistence.i_session import ISession

T = TypeVar("T")

class BaseRepository[T]:

def __init__(self, session: ISession, entity_class: type[T]) -> None:
        
        self.session = session
        self.entity_class = entity_class

    def add(self, entity: T) -> None:
        
        self.session.add(entity)

    def get_by_id(self, entity_id: Any) -> T | None:
        
        return self.session.get(self.entity_class, entity_id)

    def list_all(self) -> list[T]:
        
        return self.session.query(self.entity_class).all()

    def update(self, entity: T) -> None:
        
        self.session.merge(entity)

    def delete(self, entity: T) -> None:
        
        self.session.delete(entity)
``````

# FILE: extensions\persistence\sqlalchemy_session_adapter.py

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

# FILE: extensions\thread_manager_module.py

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.thread_manager import ThreadManager
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.infrastructure.persistence.i_thread_manager import (
    IThreadManager,
)

class ThreadManagerExtension(IExtension):

def register(self, context: "EngineContext") -> None:

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

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass

class ThreadManagerModule(ThreadManagerExtension):

def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "ThreadManagerModule is deprecated. Use ThreadManagerExtension instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
``````

# FILE: infrastructure\__init__.py

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

# FILE: infrastructure\config\__init__.py

```python
from .config_manager import ConfigManager
from .dict_config import DictConfig
from .config_source import ConfigSource
from .dict_source import DictSource
from .env_source import EnvSource
from .json_source import JsonSource

__all__ = ["ConfigManager", "DictConfig", "ConfigSource", "DictSource", "EnvSource", "JsonSource"]
``````

# FILE: infrastructure\config\config_manager.py

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

    def _load(self) -> None:
        
        if self._loaded:
            return
        self._cache = {}
        for source in self._sources:
            try:
                data = source.read()
                self._cache.update(data)
            except Exception:
                pass
        self._loaded = True

    def get(self, key: str, default: Any=None) -> Any:
        
        self._load()
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        
        self._load()
        self._cache[key] = value
``````

# FILE: infrastructure\config\config_source.py

```python
from abc import ABC, abstractmethod
from typing import Any

class ConfigSource(ABC):

@abstractmethod
    def read(self) -> dict[str, Any]:
        
        ...
``````

# FILE: infrastructure\config\config_sources\__init__.py

```python
from .dotenv_source import DotenvSource

__all__ = ["DotenvSource"]
``````

# FILE: infrastructure\config\config_sources\dotenv_source.py

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

# FILE: infrastructure\config\dict_config.py

```python
from typing import Any

from sagittarius_engine.interfaces import IConfig

class DictConfig(IConfig):

def __init__(self, initial_data: dict[str, Any] | None = None) -> None:
        
        self._config: dict[str, Any] = initial_data if initial_data is not None else {}

    def get(self, key: str, default: Any = None) -> Any:
        
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        
        self._config[key] = value
``````

# FILE: infrastructure\config\dict_source.py

```python
from typing import Any
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class DictSource(ConfigSource):

def __init__(self, data: dict[str, Any]) -> None:
        
        self.data = data

    def read(self) -> dict[str, Any]:
        
        return self.data
``````

# FILE: infrastructure\config\env_source.py

```python
import os
from typing import Any
from sagittarius_engine.infrastructure.config.config_source import ConfigSource

class EnvSource(ConfigSource):

def __init__(self, prefix: str='') -> None:
        
        self.prefix = prefix

    def read(self) -> dict[str, Any]:
        
        result = {}
        for k, v in os.environ.items():
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                result[key] = v
        return result
``````

# FILE: infrastructure\config\json_source.py

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
        except json.JSONDecodeError:
            return {}
``````

# FILE: infrastructure\container\__init__.py

```python
from .std_container import StdLibContainer

__all__ = [
    "StdLibContainer",
]
``````

# FILE: infrastructure\container\std_container.py

```python
import inspect
import threading
from collections.abc import Callable
from typing import Any, TypeVar

from sagittarius_engine.exceptions import DependencyResolutionError
from sagittarius_engine.interfaces import IContainer

T = TypeVar("T")

class StdLibContainer(IContainer):

def __init__(self) -> None:
        self._lock = threading.RLock()
        self._bindings: dict[type, type] = {}
        self._instances: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}

        self._resolution_cache: dict[type, dict[str, dict[str, Any]]] = {}

    def bind(self, abstract: type, concrete: type) -> None:
        
        with self._lock:
            self._bindings[abstract] = concrete

    def singleton(self, abstract: type, instance_or_factory: Any | Callable) -> None:
        
        with self._lock:
            if callable(instance_or_factory) and not isinstance(
                instance_or_factory, type
            ):
                self._factories[abstract] = instance_or_factory
            else:
                self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: type[T] | Any) -> T:
        
        return self._resolve(abstract, set())

    def _resolve(self, abstract: type[T] | Any, resolving: set[type]) -> T:
        
        if abstract in self._instances:
            return self._instances[abstract]

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

with self._lock:
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
                    dependencies[name] = self._resolve(param_info["annotation"], resolving)
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

# FILE: infrastructure\event_bus\__init__.py

```python
from .memory_event_bus import MemoryEventBus
from .thread_pool_event_bus import ThreadPoolEventBus
from .asyncio_event_bus import AsyncioEventBus
from .resilient_event_bus import ResilientEventBus
from .ipc_broker import IPCBroker
from .ipc_queue_event_bus import IPCQueueEventBus

__all__ = ["MemoryEventBus", "ThreadPoolEventBus", "AsyncioEventBus", "ResilientEventBus", "IPCBroker", "IPCQueueEventBus"]
``````

# FILE: infrastructure\event_bus\asyncio_event_bus.py

```python
import asyncio
import inspect
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IAsyncEventBus, ILogger

class AsyncioEventBus(IAsyncEventBus):

def __init__(self, logger: ILogger | None = None) -> None:
        
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    async def emit(self, event_name: str, data: Any = None) -> None:
        
        if self.logger:
            self.logger.info(f"Emitting async event: {event_name} with data: {data}")

        with self._lock:
            handlers_snapshot = list(self._handlers.get(event_name, []))

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
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
``````

# FILE: infrastructure\event_bus\ipc_broker.py

```python
import threading
import logging
import queue
from multiprocessing.queues import Queue
from sagittarius_engine.interfaces.i_logger import ILogger

class IPCBroker:

def __init__(self, publish_queue: Queue, logger: ILogger | None=None):
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
        self._thread = threading.Thread(target=self._run, daemon=True, name='IPCBrokerThread')
        self._thread.start()
        if self._logger:
            self._logger.info('IPCBroker started.')

    def stop(self) -> None:
        
        self._stop_event.set()
        try:
            self._publish_queue.put(('_STOP_', None))
        except Exception as e:
            if self._logger:
                self._logger.error(f'Error stopping IPCBroker: {e}')
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._logger:
            self._logger.info('IPCBroker stopped.')

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                message = self._publish_queue.get(timeout=0.1)
                if isinstance(message, tuple) and len(message) == 2 and (message[0] == '_STOP_'):
                    break
                event_name, data = message
                with self._lock:
                    for sub_queue in self._subscriber_queues:
                        try:
                            sub_queue.put((event_name, data))
                        except Exception as e:
                            if self._logger:
                                self._logger.error(f'Failed to route event {event_name} to a subscriber: {e}')
                            else:
                                logging.error(f'Failed to route event {event_name} to a subscriber: {e}')
            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f'IPCBroker encountered an error: {e}')
                else:
                    logging.error(f'IPCBroker encountered an error: {e}')
``````

# FILE: infrastructure\event_bus\ipc_queue_event_bus.py

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

def __init__(self, subscriber_queue: Queue | None=None, publish_queue: Queue | None=None, logger: ILogger | None=None):
        self._subscriber_queue = subscriber_queue
        self._publish_queue = publish_queue
        self._logger = logger
        self._handlers: dict[str, list[Callable]] = {}
        self._handlers_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def emit(self, event_name: str, data: Any=None) -> None:
        
        if not self._publish_queue:
            if self._logger:
                self._logger.warning(f"Cannot emit '{event_name}': publish_queue is None.")
            else:
                logging.warning(f"Cannot emit '{event_name}': publish_queue is None.")
            return
        try:
            self._publish_queue.put((event_name, data))
        except Exception as e:
            if self._logger:
                self._logger.error(f"Failed to emit event '{event_name}' to publish_queue: {e}")
            else:
                logging.error(f"Failed to emit event '{event_name}' to publish_queue: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        
        with self._handlers_lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        
        with self._handlers_lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
                if not self._handlers[event_name]:
                    del self._handlers[event_name]

    def start(self) -> None:
        
        if not self._subscriber_queue:
            if self._logger:
                self._logger.warning('No subscriber_queue provided; IPCQueueEventBus will not listen for events.')
            return
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name='IPCQueueEventBusListener')
        self._thread.start()
        if self._logger:
            self._logger.info('IPCQueueEventBus listener started.')

    def stop(self) -> None:
        
        self._stop_event.set()
        if self._subscriber_queue:
            try:
                self._subscriber_queue.put(('_STOP_', None))
            except Exception as e:
                if self._logger:
                    self._logger.error(f'Error stopping IPCQueueEventBus: {e}')
        if self._thread:
            self._thread.join(timeout=2.0)
        if self._logger:
            self._logger.info('IPCQueueEventBus listener stopped.')

    def _run(self) -> None:
        if not self._subscriber_queue:
            return
        while not self._stop_event.is_set():
            try:
                message = self._subscriber_queue.get(timeout=0.1)
                if isinstance(message, tuple) and len(message) == 2 and (message[0] == '_STOP_'):
                    break
                event_name, data = message
                self._dispatch(event_name, data)
            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f'IPCQueueEventBus listener error: {e}')

    def _dispatch(self, event_name: str, data: Any) -> None:
        
        with self._handlers_lock:
            handlers = self._handlers.get(event_name, []).copy()
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Error in IPC handler for '{event_name}': {e}")
``````

# FILE: infrastructure\event_bus\memory_event_bus.py

```python
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IEventBus, ILogger

class MemoryEventBus(IEventBus):

def __init__(self, logger: ILogger | None = None) -> None:
        
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    def emit(self, event_name: str, data: Any = None) -> None:
        
        if self.logger:
            self.logger.info(f"Emitting event: {event_name} with data: {data}")

        with self._lock:
            handlers_snapshot = list(self._handlers.get(event_name, []))

        for handler in handlers_snapshot:
            try:
                handler(data)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in handler {handler}: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
``````

# FILE: infrastructure\event_bus\resilient_event_bus.py

```python
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

        self._handlers: dict[str, list[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
        
        if self.logger:
            self.logger.info(
                f"Emitting resilient event: {event_name} with data: {data}"
            )

        for handler in self._handlers.get(event_name, []):
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))

    def on(self, event_name: str, handler: Callable) -> None:
        
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
        self.inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
        self.inner_bus.off(event_name, handler)

    def get_dlq(self) -> list[tuple[str, Any, Callable, Exception]]:
        
        return list(self._dlq)

    def reprocess(self) -> None:
        
        current_dlq = self._dlq
        self._dlq = []
        for event_name, data, handler, _ in current_dlq:
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))
``````

# FILE: infrastructure\event_bus\thread_pool_event_bus.py

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

    def emit(self, event_name: str, data: Any = None) -> None:
        
        if self.logger:
            self.logger.info(
                f"Emitting event: {event_name} to ThreadPoolEventBus with data: {data}"
            )

with self._inner_bus._lock:
            handlers_snapshot = list(self._inner_bus._handlers.get(event_name, []))

        futures = []
        for handler in handlers_snapshot:
            futures.append(self._executor.submit(handler, data))

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

    def on(self, event_name: str, handler: Callable) -> None:
        
        self._inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        
        self._inner_bus.off(event_name, handler)

    def shutdown(self, wait: bool = True) -> None:
        
        self._executor.shutdown(wait=wait)
``````

# FILE: infrastructure\logging\__init__.py

```python
from .std_logger import StdLogger
from .log_metrics import LogMetrics

__all__ = [
    "StdLogger",
    "LogMetrics",
]
``````

# FILE: infrastructure\logging\log_metrics.py

```python
import json

from sagittarius_engine.interfaces import ILogger
from sagittarius_engine.infrastructure.ports.i_metrics import IMetrics

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

# FILE: infrastructure\logging\std_logger.py

```python
import logging
import sys

from sagittarius_engine.interfaces import IConfig, ILogger

class StdLogger(ILogger):

def __init__(self, config: IConfig | None = None):
        
        self._logger = logging.getLogger("App")

        log_level = logging.INFO
        log_file = None

        if config:
            level_str = config.get("log.level", "INFO").upper()
            log_level = getattr(logging, level_str, logging.INFO)
            log_file = config.get("log.file")

        self._logger.setLevel(log_level)

        for handler in list(self._logger.handlers):
            handler.close()
            self._logger.removeHandler(handler)

        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

    def info(self, message: str) -> None:
        
        self._logger.info(message)

    def warning(self, message: str) -> None:
        
        self._logger.warning(message)

    def error(self, message: str) -> None:
        
        self._logger.error(message)

    def debug(self, message: str) -> None:
        
        self._logger.debug(message)
``````

# FILE: infrastructure\persistence\__init__.py

```python
from .i_session import ISession
from .i_thread_manager import IThreadManager
from .sqlalchemy_session_adapter import SQLAlchemySessionAdapter
from .database_module import DatabaseModule

__all__ = [
    "ISession",
    "IThreadManager",
    "SQLAlchemySessionAdapter",
    "DatabaseModule",
]
``````

# FILE: infrastructure\persistence\database_module.py

```python
import warnings
from sagittarius_engine.extensions.persistence.database_module import (
    DatabaseModule,
    DatabaseExtension,
    SqlAlchemyExtension,
    SQLALCHEMY_INSTALLED,
)

warnings.warn(
    "Importing DatabaseModule from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: infrastructure\persistence\i_session.py

```python
import warnings
from sagittarius_engine.extensions.persistence.i_session import ISession

warnings.warn(
    "Importing ISession from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: infrastructure\persistence\i_thread_manager.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
import concurrent.futures
from typing import Any

class IThreadManager(ABC):

@abstractmethod
    def submit(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> concurrent.futures.Future[Any]:
        
        pass

    @abstractmethod
    def shutdown(self, wait: bool = True) -> None:
        
        pass
``````

# FILE: infrastructure\persistence\sqlalchemy_session_adapter.py

```python
import warnings
from sagittarius_engine.extensions.persistence.sqlalchemy_session_adapter import (
    SQLAlchemySessionAdapter,
)

warnings.warn(
    "Importing SQLAlchemySessionAdapter from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: infrastructure\ports\__init__.py

```python
from .i_file_storage import IFileStorage
from .i_metrics import IMetrics

__all__ = [
    "IFileStorage",
    "IMetrics",
]
``````

# FILE: infrastructure\ports\i_file_storage.py

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

# FILE: infrastructure\ports\i_metrics.py

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

# FILE: infrastructure\storage\__init__.py

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

# FILE: infrastructure\storage\azure_blob_storage.py

```python
from sagittarius_engine.infrastructure.ports.i_file_storage import IFileStorage

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

# FILE: infrastructure\storage\local_file_storage.py

```python
import os

from sagittarius_engine.infrastructure.ports.i_file_storage import IFileStorage
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

# FILE: infrastructure\storage\s3_file_storage.py

```python
from sagittarius_engine.infrastructure.ports.i_file_storage import IFileStorage

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

# FILE: infrastructure\thread_manager.py

```python
import concurrent.futures
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.infrastructure.persistence.i_thread_manager import IThreadManager

class ThreadManager(IThreadManager):

def __init__(self, max_workers: int = 4) -> None:
        
        self._max_workers = max_workers
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=self._max_workers)
        self._lock = threading.Lock()

    def submit(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> concurrent.futures.Future[Any]:
        
        with self._lock:
            return self._executor.submit(task, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        
        with self._lock:
            self._executor.shutdown(wait=wait)
``````

# FILE: interfaces\__init__.py

```python
from .i_command import ICommand
from .i_query import IQuery
from .i_module import IModule
from .i_extension import IExtension
from .i_event_bus import IEventBus
from .i_async_event_bus import IAsyncEventBus
from .i_container import IContainer
from .i_middleware import IMiddleware
from .i_logger import ILogger
from .i_config import IConfig
from .i_input_port import IInputPort
from .i_output_port import IOutputPort
from .events import (
    ExtensionInitializing,
    ExtensionStarted,
    ExtensionStopped,
    ExtensionDisposed,
)

__all__ = [
    "ICommand",
    "IQuery",
    "IModule",
    "IExtension",
    "IEventBus",
    "IAsyncEventBus",
    "IContainer",
    "IMiddleware",
    "ILogger",
    "IConfig",
    "IInputPort",
    "IOutputPort",
    "ExtensionInitializing",
    "ExtensionStarted",
    "ExtensionStopped",
    "ExtensionDisposed",
]

``````

# FILE: interfaces\events.py

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

@dataclass
class HostedServiceStarted:

service_name: str

@dataclass
class HostedServiceStopped:

service_name: str

@dataclass
class TaskStarted:

task_id: str
    task_name: str

@dataclass
class TaskCompleted:

task_id: str
    task_name: str

@dataclass
class TaskFailed:

task_id: str
    task_name: str
    error: Exception

@dataclass
class SchedulerStarted:

@dataclass
class SchedulerStopped:

``````

# FILE: interfaces\i_async_event_bus.py

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

# FILE: interfaces\i_command.py

```python
import warnings
from sagittarius_engine.extensions.cqrs.commands import ICommand

warnings.warn(
    "Importing ICommand from sagittarius_engine.interfaces is deprecated. "
    "Use sagittarius_engine.extensions.cqrs instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: interfaces\i_config.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IConfig(ABC):

@abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        
        ...
``````

# FILE: interfaces\i_container.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T", bound=Any)

class IContainer(ABC):

@abstractmethod
    def bind(self, abstract: type, concrete: type) -> None:
        
        ...

    @abstractmethod
    def singleton(self, abstract: type, instance_or_factory: Any | Callable) -> None:
        
        ...

    @abstractmethod
    def resolve(self, abstract: type[T] | Any) -> T:
        
        ...
``````

# FILE: interfaces\i_event_bus.py

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

class IEventBus(ABC):

@abstractmethod
    def emit(self, event_name: str, data: Any = None) -> None:
        
        ...

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        
        ...

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        
        ...
``````

# FILE: interfaces\i_extension.py

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

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
        
        return ExtensionDescriptor(name=self.__class__.__name__)

    @abstractmethod
    def register(self, context: "EngineContext") -> None:
        
        ...

    @abstractmethod
    def boot(self, context: "EngineContext") -> None:
        
        ...

    @abstractmethod
    def shutdown(self, context: "EngineContext") -> None:
        
        ...

    def initialize(self, context: "EngineContext") -> None:
        
        self.register(context)

    def start(self, context: "EngineContext") -> None:
        
        self.boot(context)

    def stop(self, context: "EngineContext") -> None:
        
        self.shutdown(context)

    def dispose(self, context: "EngineContext") -> None:
        
        pass
``````

# FILE: interfaces\i_input_port.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IInputPort(ABC):

@abstractmethod
    def receive(self) -> dict[str, Any]:
        
        pass
``````

# FILE: interfaces\i_logger.py

```python
from abc import ABC, abstractmethod

class ILogger(ABC):

@abstractmethod
    def info(self, message: str) -> None:
        
        ...

    @abstractmethod
    def warning(self, message: str) -> None:
        
        ...

    @abstractmethod
    def error(self, message: str) -> None:
        
        ...

    @abstractmethod
    def debug(self, message: str) -> None:
        
        ...
``````

# FILE: interfaces\i_middleware.py

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

# FILE: interfaces\i_module.py

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

# FILE: interfaces\i_output_port.py

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

# FILE: interfaces\i_query.py

```python
import warnings
from sagittarius_engine.extensions.cqrs.queries import IQuery

warnings.warn(
    "Importing IQuery from sagittarius_engine.interfaces is deprecated. "
    "Use sagittarius_engine.extensions.cqrs instead.",
    DeprecationWarning,
    stacklevel=2,
)
``````

# FILE: kernel\__init__.py

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

# FILE: kernel\app_runner.py

```python
from typing import Any, Type

from sagittarius_engine.kernel import App
from sagittarius_engine.interfaces.i_command import ICommand
from sagittarius_engine.interfaces.i_input_port import IInputPort
from sagittarius_engine.interfaces.i_output_port import IOutputPort
from sagittarius_engine.interfaces.i_query import IQuery

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
        command_map: dict[str, Type[ICommand]],
        query_map: dict[str, Type[IQuery]],
    ) -> None:
        
        while True:
            try:
                input_data = self.input_port.receive()
                command_name = input_data.get(COMMAND_KEY)

                if command_name == EXIT_COMMAND:
                    break

                if command_name in command_map:
                    cmd_cls = command_map[command_name]
                    result = self.execute(cmd_cls, input_data)
                    self.output_port.present(result)
                elif command_name in query_map:
                    query_cls = query_map[command_name]
                    result = self.query(query_cls, input_data)
                    self.output_port.present(result)
                else:
                    self.output_port.present_error(
                        ValueError(f"Unknown command: {command_name}")
                    )

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.output_port.present_error(e)

    def execute(self, command_class: Type[ICommand], dto: Any = None) -> Any:
        
        return self.app.execute(command_class, dto)

    def query(self, query_class: Type[IQuery], dto: Any = None) -> Any:
        
        return self.app.query(query_class, dto)
``````

# FILE: kernel\app.py

```python
from typing import Any
from sagittarius_engine.exceptions import ModuleRegistrationError
from sagittarius_engine.kernel.context import EngineContext
from sagittarius_engine.interfaces import (
    ICommand,
    IContainer,
    IEventBus,
    ILogger,
    IMiddleware,
    IModule,
    IQuery,
)

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
    def modules(self) -> list[Any]:
        return self.context.modules

    @property
    def pipeline(self) -> Any:
        return self.context.middleware_pipeline

    @property
    def lifecycle(self) -> Any:
        return self.context.lifecycle

    def use(self, extension_or_module: Any) -> None:
        
        try:
            self.context.extension_manager.register(extension_or_module)
        except TypeError as e:
            raise ModuleRegistrationError(str(e)) from e

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        
        self.context.middleware_pipeline.add(middleware_instance)

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def boot(self, auto_discover: str | None = None) -> None:
        
        self.context.bootstrap.boot(auto_discover)

    def dispatch(self, handler_class: type, input_dto: Any = None) -> Any:
        
        return self.context.dispatcher.dispatch(handler_class, input_dto)

    def execute(self, command_class: type, input_dto: Any = None) -> Any:
        
        import warnings

        warnings.warn(
            "App.execute is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: Any = None) -> Any:
        
        import warnings

        warnings.warn(
            "App.query is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)

    def stop(self) -> None:
        
        logger = self._get_logger()
        if logger:
            logger.info("App is stopping gracefully...")

        self.context.lifecycle.set_stopping()

try:
            self.context.scheduler.stop()
        except Exception as e:
            if logger:
                logger.error(f"Error stopping scheduler: {e}")

try:
            self.context.hosted_services.stop()
        except Exception as e:
            if logger:
                logger.error(f"Error stopping hosted services: {e}")

try:
            self.context.extension_manager.stop_and_dispose()
        except Exception as e:
            if logger:
                logger.error(f"Error stopping extensions: {e}")

try:
            self.context.tasks.shutdown()
        except Exception as e:
            if logger:
                logger.error(f"Error shutting down task manager: {e}")

try:
            self.context.async_runtime.stop()
        except Exception as e:
            if logger:
                logger.error(f"Error stopping async runtime: {e}")

        self.context.lifecycle.set_stopped()
        if logger:
            logger.info("App stopped.")

``````

# FILE: kernel\bootstrap.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces import ILogger

class Bootstrap:

def __init__(self, context: Any) -> None:
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

        except Exception as e:
            if logger:
                logger.error(f"Error during boot sequence: {e}. Shutting down runtime...")

            try:
                self.context.scheduler.stop()
            except Exception:
                pass
            try:
                self.context.hosted_services.stop()
            except Exception:
                pass
            try:
                self.context.async_runtime.stop()
            except Exception:
                pass
            raise e

        self.context.lifecycle.set_booted()

        if logger:
            logger.info(
                f"App booted successfully with {len(self.context.modules)} modules."
            )

        self.context.event_bus.emit("app.booted", self.context.app)
``````

# FILE: kernel\context.py

```python
from typing import Any
from sagittarius_engine.interfaces import (
    IContainer,
    IEventBus,
    ILogger,
    IConfig,
    IModule,
)
from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
from sagittarius_engine.kernel.lifecycle import EngineLifecycle
from sagittarius_engine.kernel.module_loader import ModuleLoader
from sagittarius_engine.kernel.bootstrap import Bootstrap
from sagittarius_engine.kernel.dispatcher import Dispatcher

from sagittarius_engine.kernel.extension_manager import ExtensionManager

class EngineContext:

def __init__(self, app: Any, container: IContainer, event_bus: IEventBus) -> None:
        self.app = app
        self.container = container
        self.event_bus = event_bus
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
        self.tasks = TaskManager(self)
        self.scheduler = Scheduler(self)
        self.hosted_services = HostedServiceManager(self)

self.container.singleton(AsyncRuntime, self.async_runtime)
        self.container.singleton(TaskManager, self.tasks)
        self.container.singleton(Scheduler, self.scheduler)
        self.container.singleton(HostedServiceManager, self.hosted_services)

    @property
    def modules(self) -> list[Any]:
        return self.extension_manager.registered_extensions

    @property
    def logger(self) -> ILogger | None:
        try:
            return self.container.resolve(ILogger)
        except Exception:
            return None

    @property
    def config(self) -> IConfig | None:
        try:
            return self.container.resolve(IConfig)
        except Exception:
            return None
``````

# FILE: kernel\dispatcher.py

```python
from typing import Any
import warnings
from sagittarius_engine.interfaces import ILogger

class Dispatcher:

def __init__(self, context: Any) -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def dispatch(self, handler_class: type, input_dto: Any = None) -> Any:
        
        logger = self._get_logger()
        if logger:
            msg_type = "query" if "Query" in handler_class.__name__ else "command"
            logger.info(f"Executing {msg_type}: {handler_class.__name__}")
        handler = self.context.container.resolve(handler_class)

        def final() -> Any:
            return handler.execute(input_dto)

        return self.context.middleware_pipeline.execute(handler, input_dto, final)

    def execute(self, command_class: type, input_dto: Any = None) -> Any:
        
        warnings.warn(
            "Dispatcher.execute is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: Any = None) -> Any:
        
        warnings.warn(
            "Dispatcher.query is deprecated. Use Dispatcher.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)
``````

# FILE: kernel\extension_manager.py

```python
from typing import Any, Optional
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor
from sagittarius_engine.interfaces.i_module import IModule
from sagittarius_engine.interfaces.events import (
    ExtensionInitializing,
    ExtensionStarted,
    ExtensionStopped,
    ExtensionDisposed,
)
from sagittarius_engine.exceptions import (
    ExtensionDependencyError,
    ExtensionCircularDependencyError,
    ModuleRegistrationError,
)

class ModuleExtensionAdapter(IExtension):

def __init__(self, legacy_module: Any):
        self.legacy_module = legacy_module
        self._descriptor = ExtensionDescriptor(name=legacy_module.__class__.__name__)

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._descriptor

    def register(self, context: Any) -> None:
        self.legacy_module.register(context.app)

    def boot(self, context: Any) -> None:
        self.legacy_module.boot(context.app)

    def shutdown(self, context: Any) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self.legacy_module, name)

def create_module_extension_adapter(legacy_module: Any) -> Any:
    
    cls_name = legacy_module.__class__.__name__

    dynamic_cls = type(cls_name, (ModuleExtensionAdapter,), {})
    return dynamic_cls(legacy_module)

class ExtensionManager:

def __init__(self, context: Any) -> None:
        self.context = context
        self.registered_extensions: list[IExtension] = []
        self.sorted_extensions: list[IExtension] = []
        self.initialized_extensions: list[IExtension] = []

    def register(self, extension_or_module: Any) -> None:
        
        if isinstance(extension_or_module, IExtension):
            ext = extension_or_module
        elif isinstance(extension_or_module, IModule):
            ext = create_module_extension_adapter(extension_or_module)
        else:

            if hasattr(extension_or_module, "register") and hasattr(
                extension_or_module, "boot"
            ):
                ext = create_module_extension_adapter(extension_or_module)
            else:
                raise TypeError(
                    "Registered object must implement IExtension or IModule"
                )

        self.registered_extensions.append(ext)

try:
            self._try_initialize_available()
        except Exception as e:
            self._rollback()
            raise e

    def _get_logger(self) -> Any:
        try:
            return self.context.logger
        except Exception:
            return None

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception:
            pass

    def _try_initialize_available(self) -> None:
        
        initialized_names = {
            ext.descriptor.name for ext in self.initialized_extensions
        }
        enabled_exts = [
            ext for ext in self.registered_extensions if ext.descriptor.enabled
        ]
        ext_by_name = {ext.descriptor.name: ext for ext in enabled_exts}

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
                except Exception as e:
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

    def _rollback(self) -> None:
        
        logger = self._get_logger()
        for ext in reversed(self.initialized_extensions):
            name = ext.descriptor.name
            if logger:
                logger.info(f"Disposing extension '{name}' due to rollback...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error during rollback disposal of '{name}': {e}")

        self.initialized_extensions.clear()

    def stop_and_dispose(self) -> None:
        
        logger = self._get_logger()
        for ext in reversed(self.sorted_extensions):
            name = ext.descriptor.name
            if logger:
                logger.info(f"Stopping extension '{name}'...")
            try:
                ext.stop(self.context)
                self._emit("extension.stopped", ExtensionStopped(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error stopping extension '{name}': {e}")

            if logger:
                logger.info(f"Disposing extension '{name}'...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error disposing extension '{name}': {e}")
``````

# FILE: kernel\lifecycle.py

```python
from typing import Any

class EngineLifecycle:

def __init__(self, context: Any) -> None:
        self.context = context
        self.state = "stopped"

    def set_booting(self) -> None:
        self.state = "booting"

    def set_booted(self) -> None:
        self.state = "booted"

    def set_stopping(self) -> None:
        self.state = "stopping"

    def set_stopped(self) -> None:
        self.state = "stopped"

    @property
    def is_booted(self) -> bool:
        return self.state == "booted"

    @property
    def is_booting(self) -> bool:
        return self.state == "booting"

    @property
    def is_stopping(self) -> bool:
        return self.state == "stopping"

    @property
    def is_stopped(self) -> bool:
        return self.state == "stopped"
``````

# FILE: kernel\middleware_pipeline.py

```python
import functools
from collections.abc import Callable
from typing import Any
from sagittarius_engine.interfaces import IMiddleware

class MiddlewarePipeline:

def __init__(self) -> None:
        self.middlewares: list[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        
        self.middlewares.append(middleware)

    def execute(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any]) -> Any:

next_handler = final_handler
        for middleware in reversed(self.middlewares):
            next_handler = functools.partial(middleware.process, cmd_or_query, dto, next_handler)
        return next_handler()
``````

# FILE: kernel\module_auto_discovery.py

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

# FILE: kernel\module_loader.py

```python
import importlib
import inspect
import pkgutil
from typing import Any
from sagittarius_engine.base.base_module import BaseModule
from sagittarius_engine.interfaces import IModule, ILogger

class ModuleLoader:

def __init__(self, context_or_app: Any) -> None:
        self.context_or_app = context_or_app

    @property
    def context(self) -> Any:
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

# FILE: middleware\__init__.py

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

# FILE: middleware\logging_middleware.py

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

# FILE: middleware\pydantic_validation_middleware.py

```python
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IMiddleware

try:
    from pydantic import BaseModel, ValidationError
except ImportError:
    BaseModel = None
    ValidationError = None

class PydanticValidationMiddleware(IMiddleware):

def __init__(self, model_class: Any) -> None:
        
        if BaseModel is None:
            raise ImportError(
                "pydantic is not installed. Please install it using `pip install pydantic`."
            )
        self.model_class = model_class

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        
        try:
            if hasattr(self.model_class, "model_validate"):

                if data_transfer_obj is None:
                    validated_dto = self.model_class()
                elif isinstance(data_transfer_obj, dict):
                    validated_dto = self.model_class.model_validate(data_transfer_obj)
                elif isinstance(data_transfer_obj, self.model_class):
                    validated_dto = data_transfer_obj
                else:
                    try:
                        validated_dto = self.model_class.model_validate(data_transfer_obj)
                    except Exception:
                        dto_dict = (
                            data_transfer_obj.__dict__
                            if hasattr(data_transfer_obj, "__dict__")
                            else {}
                        )
                        validated_dto = self.model_class.model_validate(dto_dict)
            else:

                if data_transfer_obj is None:
                    validated_dto = self.model_class()
                elif isinstance(data_transfer_obj, dict):
                    validated_dto = self.model_class(**data_transfer_obj)
                elif isinstance(data_transfer_obj, self.model_class):
                    validated_dto = data_transfer_obj
                else:
                    dto_dict = (
                        data_transfer_obj.__dict__
                        if hasattr(data_transfer_obj, "__dict__")
                        else {}
                    )
                    validated_dto = self.model_class(**dto_dict)
            data_transfer_obj = validated_dto
        except ValidationError as e:
            raise ValueError(
                f"Validation failed for {cmd_or_query.__class__.__name__}: {e}"
            )

        return next_handler()
``````

# FILE: middleware\timing_middleware.py

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

# FILE: middleware\transaction_middleware.py

```python
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IContainer, IMiddleware
from sagittarius_engine.infrastructure.persistence.i_session import ISession

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

# FILE: middleware\validation_middleware.py

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

# FILE: runtime\__init__.py

```python
from .hosted import IHostedService, HostedServiceManager
from .tasks import CancellationToken, BackgroundTask, TaskManager
from .scheduler import Scheduler, ITrigger, IntervalTrigger, CronTrigger
from .async_runtime import AsyncRuntime

__all__ = [
    "IHostedService",
    "HostedServiceManager",
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

# FILE: runtime\async_runtime\__init__.py

```python
from .async_runtime import AsyncRuntime

__all__ = ["AsyncRuntime"]
``````

# FILE: runtime\async_runtime\async_runtime.py

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
        except Exception:
            pass

        self.loop.close()
        self.loop = None
        self._logger.info("AsyncRuntime event loop stopped.")
``````

# FILE: runtime\hosted\__init__.py

```python
from .hosted_service import IHostedService
from .hosted_service_manager import HostedServiceManager

__all__ = ["IHostedService", "HostedServiceManager"]
``````

# FILE: runtime\hosted\hosted_service_manager.py

```python
import logging
from typing import Any, List
from sagittarius_engine.runtime.hosted.hosted_service import IHostedService
from sagittarius_engine.interfaces.events import (
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
        except Exception:
            pass

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
            raise RuntimeError(
                f"Multiple errors stopping hosted services: {errors}"
            )
``````

# FILE: runtime\hosted\hosted_service.py

```python
from abc import ABC, abstractmethod
from typing import Any

class IHostedService(ABC):

@abstractmethod
    def start(self, context: Any) -> None:
        
        pass

    @abstractmethod
    def stop(self, context: Any) -> None:
        
        pass
``````

# FILE: runtime\scheduler\__init__.py

```python
from .scheduler import Scheduler
from .triggers import ITrigger, IntervalTrigger, CronTrigger

__all__ = ["Scheduler", "ITrigger", "IntervalTrigger", "CronTrigger"]
``````

# FILE: runtime\scheduler\scheduler.py

```python
import logging
import threading
from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional
from sagittarius_engine.runtime.scheduler.triggers import (
    ITrigger,
    IntervalTrigger,
    CronTrigger,
)
from sagittarius_engine.interfaces.events import (
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

def __init__(self, context: Any) -> None:
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
        except Exception:
            pass

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
                        self._logger.error(
                            f"Failed to spawn scheduled job: {e}"
                        )

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

# FILE: runtime\scheduler\triggers.py

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

        next_min = from_time.replace(second=0, microsecond=0) + timedelta(
            minutes=1
        )
        return next_min
``````

# FILE: runtime\tasks\__init__.py

```python
from .cancellation_token import CancellationToken
from .background_task import BackgroundTask
from .task_manager import TaskManager

__all__ = ["CancellationToken", "BackgroundTask", "TaskManager"]
``````

# FILE: runtime\tasks\background_task.py

```python
import uuid
from typing import Any, Optional
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken

class BackgroundTask:

def __init__(self, name: str, token: Optional[CancellationToken] = None) -> None:
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.token: CancellationToken = (
            token if token is not None else CancellationToken()
        )
        self.future: Optional[Any] = None
        self.status: str = "pending"
        self.error: Optional[Exception] = None

    def cancel(self) -> None:
        
        self.token.cancel()
        if self.future is not None:
            self.future.cancel()
            self.status = "cancelled"
``````

# FILE: runtime\tasks\cancellation_token.py

```python
import threading

class CancellationToken:

def __init__(self, event: threading.Event = None) -> None:
        self._event = event if event is not None else threading.Event()

    def is_cancelled(self) -> bool:
        
        return self._event.is_set()

    @property
    def is_cancellation_requested(self) -> bool:
        
        return self._event.is_set()

    def cancel(self) -> None:
        
        self._event.set()

    def wait(self, timeout: float = None) -> bool:
        
        return self._event.wait(timeout)
``````

# FILE: runtime\tasks\task_manager.py

```python
import inspect
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional, Union
from sagittarius_engine.runtime.tasks.background_task import BackgroundTask
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
from sagittarius_engine.interfaces.events import (
    TaskStarted,
    TaskCompleted,
    TaskFailed,
)

class TaskManager:

def __init__(self, context: Any) -> None:
        self.context = context
        self.tasks: Dict[str, BackgroundTask] = {}
        self.executor = ThreadPoolExecutor(
            max_workers=20, thread_name_prefix="SagittariusTask"
        )
        self._lock = threading.Lock()
        self._logger = logging.getLogger("App")

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception:
            pass

    def _cleanup_old_tasks(self) -> None:
        with self._lock:

            if len(self.tasks) > 200:
                finished_ids = [
                    tid
                    for tid, t in self.tasks.items()
                    if t.status in ("completed", "failed", "cancelled")
                ]

                for tid in finished_ids[:-50]:
                    del self.tasks[tid]

    def _wrap_sync(
        self, bg_task: BackgroundTask, fn: Callable[[], Any]
    ) -> Callable[[], Any]:
        def wrapper():
            try:
                res = fn()
                bg_task.status = "completed"
                self._emit(
                    "runtime.tasks.completed",
                    TaskCompleted(bg_task.id, bg_task.name),
                )
                return res
            except Exception as e:
                bg_task.status = "failed"
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
            bg_task.status = "completed"
            self._emit(
                "runtime.tasks.completed", TaskCompleted(bg_task.id, bg_task.name)
            )
            return res
        except Exception as e:
            bg_task.status = "failed"
            bg_task.error = e
            self._logger.error(f"Async task '{bg_task.name}' failed: {e}")
            self._emit(
                "runtime.tasks.failed", TaskFailed(bg_task.id, bg_task.name, e)
            )
            raise e
        finally:
            self._cleanup_old_tasks()

    def spawn(
        self,
        callable_or_coro: Union[Callable[..., Any], Any],
        name: Optional[str] = None,
        token: Optional[CancellationToken] = None,
    ) -> BackgroundTask:
        
        task_name = (
            name
            or (
                callable_or_coro.__name__
                if hasattr(callable_or_coro, "__name__")
                else "UnnamedTask"
            )
        )
        bg_task = BackgroundTask(task_name, token)

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
            bg_task.status = "running"
            try:
                future = self.context.async_runtime.run_coroutine(
                    self._wrap_coro(bg_task, coro)
                )
                bg_task.future = future
            except Exception as e:
                bg_task.status = "failed"
                bg_task.error = e
                self._emit(
                    "runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e)
                )
                raise e
        else:

            bg_task.status = "running"
            try:
                sig = inspect.signature(callable_or_coro)
                if "token" in sig.parameters:
                    fn = lambda: callable_or_coro(token=bg_task.token)
                else:
                    fn = lambda: callable_or_coro()

                future = self.executor.submit(self._wrap_sync(bg_task, fn))
                bg_task.future = future
            except Exception as e:
                bg_task.status = "failed"
                bg_task.error = e
                self._emit(
                    "runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e)
                )
                raise e

        return bg_task

    def cancel_all(self) -> None:
        
        with self._lock:
            for task in self.tasks.values():
                if task.status == "running":
                    task.cancel()

    def shutdown(self) -> None:
        
        self.cancel_all()
        self.executor.shutdown(wait=True)
``````

# FILE: sdk\__init__.py

```python
from .template_loader import TemplateLoader
from .template_renderer import TemplateRenderer
from .project_generator import ProjectGenerator

__all__ = ["TemplateLoader", "TemplateRenderer", "ProjectGenerator"]
``````

# FILE: sdk\project_generator.py

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
        extra_placeholders: dict[str, str] = None,
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
                    rendered_content = self.renderer.render(
                        file_content, placeholders
                    )
                    with open(dest_file_path, "w", encoding="utf-8") as f:
                        f.write(rendered_content)
                except UnicodeDecodeError:

                    shutil.copy2(src_file_path, dest_file_path)

        return project_path
``````

# FILE: sdk\template_loader.py

```python
import os
from typing import List

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
            if os.path.exists(path) and os.path.isdir(path):
                return path
        raise ValueError(f"Template '{template_name}' not found.")
``````

# FILE: sdk\template_renderer.py

```python
import re

class TemplateRenderer:

def render(self, content: str, placeholders: dict[str, str]) -> str:
        
        rendered = content
        for key, value in placeholders.items():

            pattern = re.compile(r"\{\{\s*" + re.escape(key) + r"\s*\}\}")
            rendered = pattern.sub(str(value), rendered)
        return rendered
``````

# FILE: sdk\templates\clean\adapters\__init__.py

```python

``````

# FILE: sdk\templates\clean\application\__init__.py

```python

``````

# FILE: sdk\templates\clean\domain\__init__.py

```python

``````

# FILE: sdk\templates\clean\infrastructure\__init__.py

```python

``````

# FILE: sdk\templates\clean\main.py

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

# FILE: sdk\templates\clean\modules\__init__.py

```python

``````

# FILE: sdk\templates\ddd\application\__init__.py

```python

``````

# FILE: sdk\templates\ddd\domain\model\__init__.py

```python

``````

# FILE: sdk\templates\ddd\domain\services\__init__.py

```python

``````

# FILE: sdk\templates\ddd\infrastructure\__init__.py

```python

``````

# FILE: sdk\templates\ddd\interfaces\__init__.py

```python

``````

# FILE: sdk\templates\ddd\main.py

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

# FILE: sdk\templates\minimal\main.py

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

# FILE: sdk\templates\mvc\controllers\__init__.py

```python

``````

# FILE: sdk\templates\mvc\main.py

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

# FILE: sdk\templates\mvc\models\__init__.py

```python

``````

# FILE: sdk\templates\mvc\views\__init__.py

```python

``````

# FILE: tools\__init__.py

```python

``````

# FILE: tools\scaffold.py

```python
import json
import os

def create_project(project_name: str, base_path: str = ".") -> None:
    
    project_dir = os.path.join(base_path, project_name)

for dir_name in ["domain", "application", "infrastructure", "adapters", "modules"]:
        os.makedirs(os.path.join(project_dir, dir_name), exist_ok=True)

        with open(os.path.join(project_dir, dir_name, "__init__.py"), "w") as f:
            pass

config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump({"app_name": project_name, "version": "1.0.0"}, f, indent=4)

main_py_content = 
    main_path = os.path.join(project_dir, "main.py")
    with open(main_path, "w") as f:
        f.write(main_py_content)

    print(f"Project '{project_name}' scaffolded successfully at '{project_dir}'.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        create_project(sys.argv[1])
    else:
        print("Usage: python scaffold.py <project_name>")
``````

