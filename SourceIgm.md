# PROJECT CONTEXT

**Root:** `/home/hoanganh/Documents/Sagittarius_ForkBoy/src/`
**Pattern:** `*py`
**Files:** 43
**Generated:** 2026-06-26 10:35:42

## Directory Tree

```
src
├── __init__.py
├── app_kernel.py
├── base_event.py
├── base_module.py
├── base_repository.py
├── exceptions.py
├── hot_reloader.py
├── infra
│   ├── asyncio_event_bus.py
│   ├── azure_blob_storage.py
│   ├── config_manager.py
│   ├── config_source
│   │   ├── __init__.py
│   │   └── dotenv_source.py
│   ├── dict_config.py
│   ├── local_file_storage.py
│   ├── log_metrics.py
│   ├── memory_event_bus.py
│   ├── resilient_event_bus.py
│   ├── s3_file_storage.py
│   ├── std_container.py
│   ├── std_logger.py
│   └── thread_pool_event_bus.py
├── interfaces
│   ├── __init__.py
│   ├── i_async_event_bus.py
│   ├── i_command.py
│   ├── i_config.py
│   ├── i_container.py
│   ├── i_event_bus.py
│   ├── i_file_storage.py
│   ├── i_logger.py
│   ├── i_metrics.py
│   ├── i_middleware.py
│   ├── i_module.py
│   ├── i_query.py
│   └── i_session.py
├── middleware
│   ├── logging_middleware.py
│   ├── pydantic_validation_middleware.py
│   ├── timing_middleware.py
│   └── validation_middleware.py
├── modules
│   ├── __init__.py
│   ├── database_module.py
│   ├── health_module.py
│   └── logger_module.py
└── scaffold.py
```

---

# FILE: __init__.py

```python

``````

# FILE: app_kernel.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional
import inspect
import pkgutil
import importlib

from src.interfaces import IModule, IContainer, IEventBus, IMiddleware, ICommand, IQuery, ILogger
from src.exceptions import ModuleRegistrationError, DependencyResolutionError
from src.base_module import BaseModule

class MiddlewarePipeline:
    """
    @brief Manages a chain of Middlewares.

    @details Follows the Onion execution pattern: requests go from the outside into
    the core (Command/Query), and the result returns from the inside out.
    """

    def __init__(self) -> None:
        self.middlewares: list[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        """
        @brief Appends a Middleware to the end of the chain.
        @param middleware The middleware instance to add.
        """
        self.middlewares.append(middleware)

    def execute(self, cmd_or_query: Any, data_transfer_obj: Any, final_handler: Callable[[], Any]) -> Any:
        """
        @brief Executes the entire Middleware chain.

        @param cmd_or_query The Command or Query instance.
        @param data_transfer_obj The Data Transfer Object input.
        @param final_handler The final execution handler for the Command/Query.
        @return The final execution result.
        """

        def build_chain(index: int) -> Callable[[], Any]:
            if index < len(self.middlewares):
                middleware = self.middlewares[index]
                next_handler = build_chain(index + 1)
                return lambda: middleware.process(cmd_or_query, data_transfer_obj, next_handler)
            else:
                return final_handler
        chain = build_chain(0)
        return chain()

class ModuleAutoDiscovery:
    """
    @brief Auto-discovers and loads Modules.

    @details Rules:
    - If it's a multi-file module (directory), the `__init__.py` file must act as the
      entry point and contain (or import) a class inheriting from `IModule`.
    - If it's a single-file module, the `.py` file itself must contain a class
      inheriting from `IModule`.

    @par Tutorial / Usage Example:
    @code
    # Automatically scans the "src.modules" package and registers all found IModules
    ModuleAutoDiscovery.discover("src.modules", app)
    @endcode
    """

    @staticmethod
    def discover(modules_package: str, app: 'App') -> None:
        """
        @brief Scans the specified package and loads the IModules.

        @param modules_package The string path to the modules package.
        @param app The current application instance.
        """
        try:
            package = importlib.import_module(modules_package)
        except ImportError as e:
            logger = app._get_logger()
            if logger:
                logger.warning(f"Could not discover package {modules_package}: {e}")
            return
        if not hasattr(package, '__path__'):
            return
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f'{modules_package}.{name}'
            try:
                sub_package = importlib.import_module(full_module_name)
                for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                    if issubclass(obj, IModule) and obj is not IModule and (obj is not BaseModule):
                        app.use(obj())
            except Exception:
                pass

class App:
    """
    @brief The heart of the Framework (Application Facade).

    @details App acts as the Orchestrator, connecting the Container, EventBus,
    Modules, and Middlewares together.

    @par Tutorial / Usage Example:
    @code
    # Initialize App
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Boot (can use the auto-discovery feature)
    app.boot(auto_discover="src.modules")

    # Execute a Command
    app.execute(CreateUserCommand, CreateUserDTO(name="Alice"))
    @endcode
    """

    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        """
        @brief Initializes the application with the core ports.

        @param container The dependency injection container.
        @param event_bus The event bus.
        """
        self.container = container
        self.event_bus = event_bus
        self.modules: list[IModule] = []
        self.pipeline = MiddlewarePipeline()

    def use(self, module: IModule) -> None:
        """
        @brief Manually adds a Module to the App and calls its `register` method immediately.

        @param module The module instance to add.
        @exception ModuleRegistrationError If the module does not implement IModule.
        """
        if not isinstance(module, IModule):
            raise ModuleRegistrationError('Module must implement IModule')
        self.modules.append(module)
        module.register(self)

    def use_middleware(self, middleware: IMiddleware) -> None:
        """
        @brief Registers a Middleware for the application.
        @param middleware The middleware instance.
        """
        self.pipeline.add(middleware)

    def _get_logger(self) -> Optional['ILogger']:
        try:
            return self.container.resolve(ILogger)
        except DependencyResolutionError:
            return None

    def boot(self, auto_discover: Optional[str]=None) -> None:
        """
        @brief Boots the application.

        @details The Boot process includes:
        1. Auto-discovering modules (if auto_discover is provided).
        2. Calling the `boot` method on all registered modules.
        3. Emitting the `app.booted` event to signal readiness.

        @param auto_discover The package name to auto-discover modules from.
        """
        logger = self._get_logger()
        if logger:
            logger.info('App is booting...')
        if auto_discover:
            ModuleAutoDiscovery.discover(auto_discover, self)
        for module in self.modules:
            module.boot(self)
        if logger:
            logger.info(f'App booted successfully with {len(self.modules)} modules.')
        self.event_bus.emit('app.booted', self)

    def execute(self, command_class: type[ICommand], input_dto: Any=None) -> Any:
        """
        @brief Executes a Command through the Middleware Pipeline.

        @details The App asks the Container to instantiate the Command class (including injecting
        its dependencies), then pushes it through the Middleware chain before calling `execute`.

        @param command_class The class type of the command to execute.
        @param input_dto The input data.
        @return The execution result.
        """
        logger = self._get_logger()
        if logger:
            logger.info(f'Executing command: {command_class.__name__}')
        command = self.container.resolve(command_class)

        def final() -> Any:
            return command.execute(input_dto)
        return self.pipeline.execute(command, input_dto, final)

    def query(self, query_class: type[IQuery], input_dto: Any=None) -> Any:
        """
        @brief Executes a Query through the Middleware Pipeline.

        @details Works similarly to `execute` but is intended for data retrieval operations.

        @param query_class The class type of the query to execute.
        @param input_dto The input data.
        @return The execution result.
        """
        logger = self._get_logger()
        if logger:
            logger.info(f'Executing query: {query_class.__name__}')
        query = self.container.resolve(query_class)

        def final() -> Any:
            return query.execute(input_dto)
        return self.pipeline.execute(query, input_dto, final)
``````

# FILE: base_event.py

```python
import uuid
from datetime import datetime, timezone

class BaseEvent:
    """
    @brief Base class for domain events, providing an ID and a timestamp.

    @details This class is meant to be subclassed by specific event classes to provide
    a standard set of metadata. However, there's no strict requirement to inherit from
    it; it serves as a utility.
    """
    def __init__(self) -> None:
        self.event_id: str = str(uuid.uuid4())
        self.occurred_on: datetime = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """
        @brief Returns a dictionary representation of the event.
        """
        data = self.__dict__.copy()
        data['occurred_on'] = self.occurred_on.isoformat()
        return data
``````

# FILE: base_module.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional
import inspect
import pkgutil
import importlib

from src.interfaces.i_module import IModule

class BaseModule(IModule):
    """
    @brief Base class for Modules.
    @details Provides an empty implementation (pass) for register/boot methods.
    This allows child modules to skip defining both methods if they are not needed.
    """

    def register(self, app: 'App') -> None:
        pass

    def boot(self, app: 'App') -> None:
        pass
``````

# FILE: base_repository.py

```python
from typing import Generic, TypeVar, Any, List, Optional
from src.interfaces import ISession

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    @brief Base generic Repository for entity CRUD operations.

    @details Provides standard add, get_by_id, list_all, update, and delete methods.
    Requires an ISession instance to perform database operations.

    @par Tutorial / Usage Example:
    @code
    class UserRepository(BaseRepository[User]):
        def __init__(self, session: ISession):
            super().__init__(session, User)

    # Usage:
    # user_repo = UserRepository(session)
    # user_repo.add(User(name="Alice"))
    # user = user_repo.get_by_id(1)
    @endcode
    """

    def __init__(self, session: ISession, entity_class: type[T]) -> None:
        """
        @brief Constructor.

        @param session The database session.
        @param entity_class The class of the entity this repository manages.
        """
        self.session = session
        self.entity_class = entity_class

    def add(self, entity: T) -> None:
        """
        @brief Adds a new entity to the database.
        @param entity The entity to add.
        """
        # Note: Depending on the underlying session type (e.g. SQLAlchemy),
        # we might need to access the underlying session object if ISession doesn't expose add.
        # Here we assume the adapter or session has an `add` method, or we use `execute`.
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'add'):
            self.session.session.add(entity)
        else:
            raise NotImplementedError("Session does not support 'add' operation.")

    def get_by_id(self, entity_id: Any) -> Optional[T]:
        """
        @brief Retrieves an entity by its ID.

        @param entity_id The ID of the entity.
        @return The entity if found, otherwise None.
        """
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'get'):
            return self.session.session.get(self.entity_class, entity_id)
        elif hasattr(self.session, 'query'):
            # Fallback for older SQLAlchemy versions
            return self.session.query(self.entity_class).get(entity_id)
        else:
            raise NotImplementedError("Session does not support 'get' operation.")

    def list_all(self) -> List[T]:
        """
        @brief Lists all entities of this type.
        @return A list of entities.
        """
        if hasattr(self.session, 'query'):
            return self.session.query(self.entity_class).all()
        else:
            raise NotImplementedError("Session does not support 'query' operation.")

    def update(self, entity: T) -> None:
        """
        @brief Updates an existing entity.
        @param entity The entity to update.
        """
        # In many ORMs like SQLAlchemy, objects attached to the session are automatically updated on commit.
        # If explicit merge/update is needed:
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'merge'):
            self.session.session.merge(entity)
        else:
            pass # Trust session tracking

    def delete(self, entity: T) -> None:
        """
        @brief Deletes an entity.
        @param entity The entity to delete.
        """
        if hasattr(self.session, 'session') and hasattr(self.session.session, 'delete'):
            self.session.session.delete(entity)
        else:
            raise NotImplementedError("Session does not support 'delete' operation.")
``````

# FILE: exceptions.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class ModuleRegistrationError(Exception):
    """@brief Error raised when a module fails to register."""
    pass

class DependencyResolutionError(Exception):
    """@brief Error raised when the Container fails to resolve a dependency."""
    pass
``````

# FILE: hot_reloader.py

```python
import os
import sys
import time
import threading
from typing import List

class HotReloader:
    """
    @brief Developer Experience tool to automatically restart the application when code changes.

    @details Uses a background thread to poll `os.stat` on all python files in the watched directories.
    When a modification is detected, it uses `os.execv` to restart the entire process.
    This provides a clean state restart, avoiding module caching issues.

    @par Tutorial / Usage Example:
    @code
    from src.hot_reloader import HotReloader

    if __name__ == "__main__":
        if "--watch" in sys.argv:
            reloader = HotReloader(["src", "modules", "main.py"])
            reloader.start()
        main()
    @endcode
    """
    def __init__(self, watch_paths: List[str], interval: float = 1.0) -> None:
        """
        @brief Constructor.

        @param watch_paths A list of directories or files to watch.
        @param interval The polling interval in seconds.
        """
        self.watch_paths = watch_paths
        self.interval = interval
        self._mtimes = {}
        self._running = False
        self._thread = None

    def _get_mtime(self, path: str) -> float:
        return os.stat(path).st_mtime

    def _scan_files(self) -> dict:
        mtimes = {}
        for path in self.watch_paths:
            if not os.path.exists(path):
                continue
            if os.path.isfile(path):
                if path.endswith('.py'):
                    mtimes[path] = self._get_mtime(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith('.py'):
                            full_path = os.path.join(root, file)
                            mtimes[full_path] = self._get_mtime(full_path)
        return mtimes

    def _poll(self) -> None:
        self._mtimes = self._scan_files()
        while self._running:
            time.sleep(self.interval)
            current_mtimes = self._scan_files()
            for path, mtime in current_mtimes.items():
                if path not in self._mtimes or self._mtimes[path] != mtime:
                    print(f"\n[HotReloader] Detected change in '{path}'. Restarting...\n")
                    self._restart()

            # Check for deleted files
            for path in self._mtimes:
                if path not in current_mtimes:
                    print(f"\n[HotReloader] Detected deleted file '{path}'. Restarting...\n")
                    self._restart()

            self._mtimes = current_mtimes

    def _restart(self) -> None:
        """@brief Restarts the current process."""
        sys.stdout.flush()
        sys.stderr.flush()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def start(self) -> None:
        """@brief Starts the hot reloader background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        print(f"[HotReloader] Watching directories: {', '.join(self.watch_paths)} for changes...")

    def stop(self) -> None:
        """@brief Stops the hot reloader."""
        self._running = False
        if self._thread:
            self._thread.join()
``````

# FILE: infra/asyncio_event_bus.py

```python
import asyncio
import threading
from typing import Any, Callable, Optional
from src.interfaces import IAsyncEventBus, ILogger

class AsyncioEventBus(IAsyncEventBus):
    """
    @brief Asynchronous EventBus implementation using asyncio.

    @details Allows handlers to be standard sync functions or async coroutines.
    Handlers are awaited sequentially within the asyncio event loop.
    """
    def __init__(self, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.
        @param logger Optional logger instance.
        """
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    async def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Asynchronously emits an event to all listening handlers sequentially.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting async event: {event_name} with data: {data}")

        with self._lock:
            handlers_snapshot = list(self._handlers.get(event_name, []))

        for handler in handlers_snapshot:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except asyncio.CancelledError as e:
                if self.logger:
                    self.logger.error(f"Async handler cancelled for event {event_name}: {e}")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error executing async handler for event {event_name}: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function (can be sync or async).
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
``````

# FILE: infra/azure_blob_storage.py

```python
from typing import Union
from src.interfaces import IFileStorage

try:
    from azure.storage.blob import BlobServiceClient
    from azure.core.exceptions import ResourceNotFoundError
    AZURE_INSTALLED = True
except ImportError:
    AZURE_INSTALLED = False

class AzureBlobStorage(IFileStorage):
    """
    @brief File Storage implementation for Azure Blob Storage.

    @par Requirement:
    Requires the `azure-storage-blob` package to be installed.
    """

    def __init__(self, connection_string: str, container_name: str) -> None:
        """
        @brief Constructor.
        @param connection_string The Azure Storage connection string.
        @param container_name The name of the Blob container.
        """
        if not AZURE_INSTALLED:
            raise ImportError("azure-storage-blob is not installed. Please install it using `pip install azure-storage-blob`.")

        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def read(self, path: str) -> bytes:
        """@brief Reads a blob from Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        return blob_client.download_blob().readall()

    def write(self, path: str, data: Union[bytes, str]) -> None:
        """@brief Writes data to Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        body = data.encode('utf-8') if isinstance(data, str) else data
        blob_client.upload_blob(body, overwrite=True)

    def delete(self, path: str) -> None:
        """@brief Deletes a blob from Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        blob_client.delete_blob()

    def exists(self, path: str) -> bool:
        """@brief Checks if a blob exists in Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        try:
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False
``````

# FILE: infra/config_manager.py

```python
import os
import json
from abc import ABC, abstractmethod
from typing import Any
from src.interfaces import IConfig

class ConfigSource(ABC):
    """
    @brief Configuration Source (Dict, Env, Json).
    """
    @abstractmethod
    def read(self) -> dict[str, Any]:
        """
        @brief Reads the configuration from the source.
        @return A dictionary containing the configuration data.
        """
        ...

class DictSource(ConfigSource):
    """
    @brief Configuration source from a provided Python Dictionary.
    """
    def __init__(self, data: dict[str, Any]) -> None:
        """
        @brief Constructor.
        @param data The dictionary data.
        """
        self.data = data

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from the dictionary."""
        return self.data

class EnvSource(ConfigSource):
    """
    @brief Configuration source from Environment Variables.

    @details Example: EnvSource(prefix="APP_") will read the `APP_HOST` variable and store it with the key `HOST`.
    """
    def __init__(self, prefix: str = "") -> None:
        """
        @brief Constructor.
        @param prefix The prefix to filter environment variables by.
        """
        self.prefix = prefix

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from environment variables."""
        result = {}
        for k, v in os.environ.items():
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                result[key] = v
        return result

class JsonSource(ConfigSource):
    """
    @brief Configuration source from a JSON file.
    """
    def __init__(self, filepath: str) -> None:
        """
        @brief Constructor.
        @param filepath The path to the JSON file.
        """
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from the JSON file."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

class ConfigManager(IConfig):
    """
    @brief Multi-layer configuration manager.

    @details Reads configurations from multiple sources and merges them.
    Sources added later will override the configurations of previously added sources.

    @par Tutorial / Usage Example:
    @code
    config = ConfigManager()

    # Add default JSON file
    config.add_source(JsonSource("default_config.json"))

    # Environment variables will override JSON configurations
    config.add_source(EnvSource(prefix="MYAPP_"))

    db_host = config.get("DB_HOST", "localhost")
    @endcode
    """
    def __init__(self) -> None:
        """@brief Constructor."""
        self._sources: list[ConfigSource] = []
        self._cache: dict[str, Any] = {}
        self._loaded = False

    def add_source(self, source: ConfigSource) -> None:
        """
        @brief Adds a configuration source to the manager.
        @param source The configuration source to add.
        """
        self._sources.append(source)
        self._loaded = False

    def _load(self) -> None:
        """@brief Loads and merges configurations from all sources."""
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

    def get(self, key: str, default: Any = None) -> Any:
        """
        @brief Gets a configuration value.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @return The configuration value.
        """
        self._load()
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        self._load()
        self._cache[key] = value
``````

# FILE: infra/config_source/__init__.py

```python
from .dotenv_source import DotenvSource
__all__ = ['DotenvSource']
``````

# FILE: infra/config_source/dotenv_source.py

```python
import os
from typing import Any
from src.infra.config_manager import ConfigSource

try:
    from dotenv import load_dotenv
    DOTENV_INSTALLED = True
except ImportError:
    DOTENV_INSTALLED = False

class DotenvSource(ConfigSource):
    """
    @brief Configuration source from a .env file.

    @details Uses the `python-dotenv` package to load the .env file into os.environ.
    If `python-dotenv` is not installed, it falls back to parsing the file manually.

    @par Requirement:
    It is recommended to install `python-dotenv`.

    @par Tutorial / Usage Example:
    @code
    config = ConfigManager()
    config.add_source(DotenvSource(".env"))

    db_host = config.get("DB_HOST")
    @endcode
    """
    def __init__(self, filepath: str = ".env") -> None:
        """
        @brief Constructor.
        @param filepath The path to the .env file.
        """
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from the .env file."""
        if not os.path.exists(self.filepath):
            return {}

        result = {}
        if DOTENV_INSTALLED:
            load_dotenv(dotenv_path=self.filepath)
            # After load_dotenv, the vars are in os.environ.
            # We don't want to return all of os.environ, only what we read,
            # but load_dotenv doesn't return a dict directly.
            # We can use dotenv_values for a dict.
            from dotenv import dotenv_values
            return dotenv_values(dotenv_path=self.filepath)
        else:
            # Fallback manual parsing
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip()
                        # Remove quotes if present
                        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                            v = v[1:-1]
                        result[k] = v
                        # Also set in os.environ for consistency
                        os.environ[k] = v
        return result
``````

# FILE: infra/dict_config.py

```python
from typing import Any
from src.interfaces import IConfig

class DictConfig(IConfig):
    """
    @brief A simple implementation of IConfig that stores configurations in memory (Dictionary).

    @details Suitable for use in Tests or very small applications.

    @par Tutorial / Usage Example:
    @code
    config = DictConfig()
    config.set("db.host", "127.0.0.1")
    print(config.get("db.host"))
    @endcode
    """
    def __init__(self) -> None:
        """@brief Constructor."""
        self._config: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        @brief Gets a configuration value.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @return The configuration value.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        self._config[key] = value
``````

# FILE: infra/local_file_storage.py

```python
import os
import shutil
from typing import Union
from src.interfaces import IFileStorage

class LocalFileStorage(IFileStorage):
    """
    @brief File Storage implementation for the Local File System.
    """

    def __init__(self, base_path: str = "") -> None:
        """
        @brief Constructor.
        @param base_path The base directory for file operations. Defaults to current directory.
        """
        self.base_path = base_path

    def _get_full_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)

    def read(self, path: str) -> bytes:
        """@brief Reads a file from local storage."""
        full_path = self._get_full_path(path)
        with open(full_path, 'rb') as f:
            return f.read()

    def write(self, path: str, data: Union[bytes, str]) -> None:
        """@brief Writes data to local storage. Creates directories if necessary."""
        full_path = self._get_full_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        mode = 'wb' if isinstance(data, bytes) else 'w'
        with open(full_path, mode) as f:
            f.write(data)

    def delete(self, path: str) -> None:
        """@brief Deletes a file from local storage."""
        full_path = self._get_full_path(path)
        if os.path.exists(full_path):
            os.remove(full_path)

    def exists(self, path: str) -> bool:
        """@brief Checks if a file exists in local storage."""
        return os.path.exists(self._get_full_path(path))
``````

# FILE: infra/log_metrics.py

```python
import json
from typing import Optional, Dict
from src.interfaces import IMetrics, ILogger

class LogMetrics(IMetrics):
    """
    @brief Basic implementation of IMetrics that outputs metrics to the ILogger.
    """
    def __init__(self, logger: ILogger) -> None:
        """
        @brief Constructor.
        @param logger The logger instance to use for writing metrics.
        """
        self.logger = logger

    def _format_tags(self, tags: Optional[Dict[str, str]]) -> str:
        if not tags:
            return ""
        return " " + json.dumps(tags)

    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=counter name={name} value={value}{tag_str}")

    def record_timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=timing name={name} duration_ms={duration_ms}{tag_str}")

    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=gauge name={name} value={value}{tag_str}")
``````

# FILE: infra/memory_event_bus.py

```python
import threading
from typing import Any, Callable, Optional
from src.interfaces import IEventBus, ILogger

class MemoryEventBus(IEventBus):
    """
    @brief Synchronous In-memory implementation of IEventBus.

    @details Suitable for single-process applications or in test environments.
    When an event is emitted, all registered handlers are invoked immediately
    in the same thread.

    @par Tutorial / Usage Example:
    @code
    bus = MemoryEventBus(logger)

    # Handler function
    def send_email(data):
        print(f"Sending email to {data['email']}")

    # Subscription
    bus.on('user.registered', send_email)

    # Emit event
    bus.emit('user.registered', {'email': 'test@example.com'})
    @endcode
    """
    def __init__(self, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.
        @param logger Optional logger instance.
        """
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Synchronously emits an event to all listening handlers.

        @param event_name The name of the event.
        @param data The data payload.
        """
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
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
``````

# FILE: infra/resilient_event_bus.py

```python
from typing import Any, Callable, List, Tuple, Optional
from src.interfaces import IEventBus, ILogger

class ResilientEventBus(IEventBus):
    """
    @brief A Decorator for IEventBus that adds Retry mechanisms and a Dead Letter Queue (DLQ).

    @details If a handler throws an exception while processing an event, the ResilientEventBus
    will attempt to call the handler again (Retry). If the max retries are exceeded,
    the event is pushed into the DLQ for manual processing later (Reprocess).

    @par Tutorial / Usage Example:
    @code
    # Wrap a basic event bus
    base_bus = MemoryEventBus()
    safe_bus = ResilientEventBus(inner_bus=base_bus, max_retries=3)

    # If an emit consistently fails, it goes to the DLQ
    safe_bus.emit("some.event", data)

    # Inspect failed events
    failed_events = safe_bus.get_dlq()

    # Attempt to re-run the failed events
    safe_bus.reprocess()
    @endcode
    """
    def __init__(self, inner_bus: IEventBus, max_retries: int = 3, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.

        @param inner_bus The base event bus to decorate.
        @param max_retries The maximum number of retries before adding to DLQ.
        @param logger Optional logger instance.
        """
        self.inner_bus = inner_bus
        self.max_retries = max_retries
        self._dlq: List[Tuple[str, Any, Callable, Exception]] = []
        self.logger = logger

        self._handlers: dict[str, list[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Emits an event with a built-in retry mechanism.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting resilient event: {event_name} with data: {data}")

        for handler in self._handlers.get(event_name, []):
            success = False
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    success = True
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
        self.inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
        self.inner_bus.off(event_name, handler)

    def get_dlq(self) -> List[Tuple[str, Any, Callable, Exception]]:
        """
        @brief Retrieves the Dead Letter Queue.
        @return A list of failed events stored in the DLQ.
        """
        return list(self._dlq)

    def reprocess(self) -> None:
        """
        @brief Attempts to reprocess all events currently in the DLQ.
        """
        current_dlq = self._dlq
        self._dlq = []
        for event_name, data, handler, _ in current_dlq:
            success = False
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    success = True
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))
``````

# FILE: infra/s3_file_storage.py

```python
from typing import Union
from src.interfaces import IFileStorage

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_INSTALLED = True
except ImportError:
    BOTO3_INSTALLED = False

class S3FileStorage(IFileStorage):
    """
    @brief File Storage implementation for AWS S3.

    @par Requirement:
    Requires the `boto3` package to be installed.
    """

    def __init__(self, bucket_name: str) -> None:
        """
        @brief Constructor.
        @param bucket_name The name of the S3 bucket.
        """
        if not BOTO3_INSTALLED:
            raise ImportError("boto3 is not installed. Please install it using `pip install boto3`.")
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def read(self, path: str) -> bytes:
        """@brief Reads a file from S3."""
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=path)
        return response['Body'].read()

    def write(self, path: str, data: Union[bytes, str]) -> None:
        """@brief Writes data to S3."""
        body = data.encode('utf-8') if isinstance(data, str) else data
        self.s3_client.put_object(Bucket=self.bucket_name, Key=path, Body=body)

    def delete(self, path: str) -> None:
        """@brief Deletes a file from S3."""
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)

    def exists(self, path: str) -> bool:
        """@brief Checks if a file exists in S3."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            raise
``````

# FILE: infra/std_container.py

```python
import inspect
from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

from src.exceptions import DependencyResolutionError
from src.interfaces import IContainer

class StdLibContainer(IContainer):
    """
    @brief Dependency Injection Container using the Python Standard Library (`inspect`).

    @details Responsible for automatically resolving dependencies for classes.
    The Container reads Type Hints (Type Annotations) in the `__init__` method to know
    what dependencies a class requires, then automatically instantiates and injects them.

    @par Tutorial / Usage Example:
    @code
    container = StdLibContainer()

    # 1. Register a Singleton (A single shared instance)
    container.singleton(IEventBus, MemoryEventBus())

    # 2. Register a standard Binding (A new instance is created on each resolve)
    container.bind(IUserRepository, PostgresUserRepository)

    # 3. Use a factory function if initialization is complex
    def make_db(container):
        return DatabaseConnection(host="localhost")
    container.singleton(DatabaseConnection, make_db)

    # 4. Resolve (Automatic dependency injection)
    # If CommandA requires IUserRepository in __init__, the container will
    # automatically fetch PostgresUserRepository and pass it in.
    command = container.resolve(CommandA)
    @endcode
    """
    def __init__(self) -> None:
        self._bindings: dict[type, type] = {}
        self._instances: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}

    def bind(self, abstract: type, concrete: type) -> None:
        """
        @brief Registers a mapping between an Interface and a concrete Class (Transient).

        @param abstract The abstract interface or class.
        @param concrete The concrete class to bind.
        """
        self._bindings[abstract] = concrete

    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        """
        @brief Registers an existing instance or a Factory function (executed once).

        @param abstract The abstract interface or class.
        @param instance_or_factory The existing instance or factory function.
        """
        if callable(instance_or_factory) and not isinstance(instance_or_factory, type):
            self._factories[abstract] = instance_or_factory
        else:
            self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: type[T]) -> T:
        """
        @brief Resolves and retrieves an instance of the requested type.
        @details This function recursively resolves the entire dependency tree.

        @param abstract The class type to resolve.
        @return An instance of the requested type.
        @exception DependencyResolutionError If the container cannot resolve a dependency.
        """
        if abstract in self._instances:
            return self._instances[abstract]

        if abstract in self._factories:
            instance = self._factories[abstract](self)
            self._instances[abstract] = instance
            return instance

        concrete = self._bindings.get(abstract, abstract)

        if not inspect.isclass(concrete):
            raise DependencyResolutionError(f"Cannot resolve {abstract}")

        if getattr(concrete, "__abstractmethods__", None):
            raise DependencyResolutionError(f"Cannot instantiate abstract class {concrete}")

        if getattr(concrete, "__init__", None) is object.__init__:
            return concrete()

        try:
            signature = inspect.signature(concrete.__init__)
        except ValueError:
            return concrete()

        dependencies = {}
        for name, param in signature.parameters.items():
            if name == 'self' or name == 'args' or name == 'kwargs':
                continue
            if param.annotation == inspect.Parameter.empty:
                raise DependencyResolutionError(f"Missing type hint for parameter '{name}' in {concrete.__name__}")
            try:
                dependencies[name] = self.resolve(param.annotation)
            except Exception as e:
                if param.default is not inspect.Parameter.empty:
                    dependencies[name] = param.default
                else:
                    raise DependencyResolutionError(f"Failed to resolve \x27{name}\x27 for {concrete.__name__}: {str(e)}")

        instance = concrete(**dependencies)
        return instance
``````

# FILE: infra/std_logger.py

```python
import logging
import sys
from typing import Optional
from src.interfaces import ILogger, IConfig

class StdLogger(ILogger):
    """
    @brief Implementation of ILogger using the default Python `logging` module.

    @details Automatically reads the IConfig (if provided) to set the log level and log file.

    @par Tutorial / Usage Example:
    @code
    config = DictConfig()
    config.set("log.level", "DEBUG")
    config.set("log.file", "app.log")

    logger = StdLogger(config)
    logger.info("System initializing")
    logger.error("DB connection error")
    @endcode
    """
    def __init__(self, config: Optional[IConfig] = None):
        """
        @brief Constructor.
        @param config Optional configuration instance.
        """
        self._logger = logging.getLogger("App")

        log_level = logging.INFO
        log_file = None

        if config:
            level_str = config.get("log.level", "INFO").upper()
            log_level = getattr(logging, level_str, logging.INFO)
            log_file = config.get("log.file")

        self._logger.setLevel(log_level)
        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

    def info(self, message: str) -> None:
        """
        @brief Logs an informational message.
        @param message The message to log.
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """
        @brief Logs a warning message.
        @param message The message to log.
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        @brief Logs an error message.
        @param message The message to log.
        """
        self._logger.error(message)

    def debug(self, message: str) -> None:
        """
        @brief Logs a debug message.
        @param message The message to log.
        """
        self._logger.debug(message)
``````

# FILE: infra/thread_pool_event_bus.py

```python
import concurrent.futures
from typing import Any, Callable, Optional
from src.interfaces import IEventBus, ILogger
from src.infra.memory_event_bus import MemoryEventBus

class ThreadPoolEventBus(IEventBus):
    """
    @brief EventBus implementation that executes handlers in a ThreadPoolExecutor.

    @details Internally uses a thread-safe MemoryEventBus to manage handlers.
    When an event is emitted, handlers are submitted to a thread pool for execution.
    """
    def __init__(self, max_workers: int = 4, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.
        @param max_workers Maximum number of threads in the pool.
        @param logger Optional logger instance.
        """
        self._inner_bus = MemoryEventBus(logger=None) # We will manage logging locally for the pool
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logger

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Emits an event, executing its handlers concurrently in a thread pool.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting event: {event_name} to ThreadPoolEventBus with data: {data}")

        # Snapshot handlers using inner bus lock
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
                        self.logger.error(f"Error executing handler for event {event}: {exc}")
            future.add_done_callback(_log_error)

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        self._inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        self._inner_bus.off(event_name, handler)

    def shutdown(self, wait: bool = True) -> None:
        """
        @brief Shuts down the thread pool executor.

        @param wait Whether to wait for pending futures to complete.
        """
        self._executor.shutdown(wait=wait)
``````

# FILE: interfaces/__init__.py

```python
from .i_metrics import IMetrics
from .i_file_storage import IFileStorage
from .i_session import ISession
from .i_command import ICommand
from .i_query import IQuery
from .i_module import IModule
from .i_event_bus import IEventBus
from .i_async_event_bus import IAsyncEventBus
from .i_container import IContainer
from .i_middleware import IMiddleware
from .i_logger import ILogger
from .i_config import IConfig

__all__ = ['ICommand', 'IQuery', 'IModule', 'IEventBus', 'IContainer', 'IMiddleware', 'ILogger', 'IConfig', 'ISession', 'IFileStorage', 'IMetrics']
``````

# FILE: interfaces/i_async_event_bus.py

```python
from typing import Any, Callable, Protocol

class IAsyncEventBus(Protocol):
    """
    @brief Asynchronous EventBus interface for decoupled communication.
    """

    async def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Asynchronously emits an event to all registered handlers.
        """
        ...

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler for a specific event.
        """
        ...

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler for a specific event.
        """
        ...
``````

# FILE: interfaces/i_command.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class ICommand(ABC):
    """
    @brief Interface for Commands in the CQRS architecture.

    @details A Command is responsible for executing operations that change the system's state
    (Write operations), such as Create, Update, or Delete.

    @par Tutorial / Usage Example:
    @code
    class CreateUserCommand(ICommand):
        def execute(self, input_dto: CreateUserDTO) -> User:
            # Logic to save user to the database goes here
            pass
    @endcode
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        @brief Executes the command.

        @param input_dto The input Data Transfer Object to be processed.
        @return The execution result (if any).
        """
        ...
``````

# FILE: interfaces/i_config.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IConfig(ABC):
    """
    @brief Interface for Configuration management.
    """

    @abstractmethod
    def get(self, key: str, default: Any=None) -> Any:
        """
        @brief Gets a configuration value.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @return The configuration value.
        """
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        ...
``````

# FILE: interfaces/i_container.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

T = TypeVar('T')

class IContainer(ABC):
    """
    @brief Interface for the Dependency Injection Container.

    @details The Container manages the initialization and distribution of dependencies.
    Instead of manually instantiating classes (e.g., new ClassA()), the Container
    automatically resolves them.

    @par Tutorial / Usage Example:
    @code
    container = StdLibContainer()
    container.bind(IUserRepository, PostgresUserRepository)

    # Get an instance (Dependencies are automatically resolved if any)
    repo = container.resolve(IUserRepository)
    @endcode
    """

    @abstractmethod
    def bind(self, abstract: type, concrete: type) -> None:
        """
        @brief Binds an Interface to a specific Implementation.
        @details A new instance is created every time it is resolved (Transient).

        @param abstract The interface or abstract class type.
        @param concrete The concrete class type to instantiate.
        """
        ...

    @abstractmethod
    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        """
        @brief Registers a Singleton.
        @details The instance is created once and reused for all subsequent resolve requests.

        @param abstract The interface or abstract class type.
        @param instance_or_factory The existing instance or a factory function.
        """
        ...

    @abstractmethod
    def resolve(self, abstract: type[T]) -> T:
        """
        @brief Resolves and returns an instance of the requested type.

        @param abstract The class type to resolve.
        @return An instance of the requested type.
        """
        ...
``````

# FILE: interfaces/i_event_bus.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IEventBus(ABC):
    """
    @brief Interface for the Event Bus (Pub/Sub mechanism).

    @details Allows different parts of the system to communicate loosely coupled.

    @par Tutorial / Usage Example:
    @code
    def on_user_created(user):
        print(f"Sending welcome email to {user.email}")

    event_bus.on("user.created", on_user_created)
    event_bus.emit("user.created", new_user_obj)
    @endcode
    """

    @abstractmethod
    def emit(self, event_name: str, data: Any=None) -> None:
        """
        @brief Publishes an event along with optional data.

        @param event_name The name of the event to emit.
        @param data The data payload to pass to handlers.
        """
        ...

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Subscribes a handler function to an event.

        @param event_name The name of the event.
        @param handler The function to call when the event occurs.
        """
        ...

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unsubscribes a handler function from an event.

        @param event_name The name of the event.
        @param handler The function to remove.
        """
        ...
``````

# FILE: interfaces/i_file_storage.py

```python
from abc import ABC, abstractmethod
from typing import Union

class IFileStorage(ABC):
    """
    @brief Interface for File Storage operations.

    @details Provides an abstraction over different storage mechanisms
    (e.g., Local File System, AWS S3, Azure Blob Storage).
    """

    @abstractmethod
    def read(self, path: str) -> bytes:
        """
        @brief Reads a file from storage.

        @param path The path or key of the file.
        @return The file content as bytes.
        """
        ...

    @abstractmethod
    def write(self, path: str, data: Union[bytes, str]) -> None:
        """
        @brief Writes data to a file in storage.

        @param path The path or key of the file.
        @param data The data to write.
        """
        ...

    @abstractmethod
    def delete(self, path: str) -> None:
        """
        @brief Deletes a file from storage.

        @param path The path or key of the file to delete.
        """
        ...

    @abstractmethod
    def exists(self, path: str) -> bool:
        """
        @brief Checks if a file exists in storage.

        @param path The path or key of the file.
        @return True if the file exists, False otherwise.
        """
        ...
``````

# FILE: interfaces/i_logger.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class ILogger(ABC):
    """
    @brief Interface for the Logging system.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        """@brief Logs an informational message."""
        ...

    @abstractmethod
    def warning(self, message: str) -> None:
        """@brief Logs a warning message."""
        ...

    @abstractmethod
    def error(self, message: str) -> None:
        """@brief Logs an error message."""
        ...

    @abstractmethod
    def debug(self, message: str) -> None:
        """@brief Logs a debug message."""
        ...
``````

# FILE: interfaces/i_metrics.py

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict

class IMetrics(ABC):
    """
    @brief Interface for Application Metrics.

    @details Provides methods to record metrics such as counters, timings, and gauges.
    """

    @abstractmethod
    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Increments a counter metric.

        @param name The name of the metric.
        @param value The value to increment by.
        @param tags Optional tags/labels for the metric.
        """
        ...

    @abstractmethod
    def record_timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Records a timing/duration metric.

        @param name The name of the metric.
        @param duration_ms The duration in milliseconds.
        @param tags Optional tags/labels for the metric.
        """
        ...

    @abstractmethod
    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Sets a gauge metric to a specific value.

        @param name The name of the metric.
        @param value The value to set.
        @param tags Optional tags/labels for the metric.
        """
        ...
``````

# FILE: interfaces/i_middleware.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IMiddleware(ABC):
    """
    @brief Interface for Middleware.

    @details Middleware acts as filters that run before and after the execution of
    a Command or Query. Highly useful for Logging, Validation, Authorization.

    @par Tutorial / Usage Example:
    @code
    class MyMiddleware(IMiddleware):
        def process(self, cmd_or_query, data_transfer_obj, next_handler):
            print("Before executing the command")
            result = next_handler()  # Calls the next handler or the main command
            print("After executing the command")
            return result
    @endcode
    """

    @abstractmethod
    def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The Data Transfer Object input.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        ...
``````

# FILE: interfaces/i_module.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IModule(ABC):
    """
    @brief Interface for application Modules.

    @details A Module is an independent organizational unit (like a plugin) that can contain
    controllers, services, repositories, commands, queries, etc.

    @par Tutorial / Usage Example:
    @code
    # 1. Create a class inheriting from IModule (or BaseModule for convenience).
    # 2. Override the `register` method to bind dependencies into the Container.
    # 3. Override the `boot` method to listen for events or setup logic on startup.
    @endcode
    """

    @abstractmethod
    def register(self, app: 'App') -> None:
        """
        @brief Called first when the module is added to the App.
        @details Used to register components (services, repositories) into the DI Container.

        @param app The current application instance.
        """
        ...

    @abstractmethod
    def boot(self, app: 'App') -> None:
        """
        @brief Called after all modules have been registered.
        @details Used to initialize connections, register event listeners, etc.

        @param app The current application instance.
        """
        ...
``````

# FILE: interfaces/i_query.py

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IQuery(ABC):
    """
    @brief Interface for Queries in the CQRS architecture.

    @details A Query is responsible for fetching data from the system WITHOUT changing its state
    (Read-only operations).

    @par Tutorial / Usage Example:
    @code
    class GetUserQuery(IQuery):
        def execute(self, input_dto: GetUserDTO) -> User:
            # Logic to query the database goes here
            pass
    @endcode
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        @brief Executes the query.

        @param input_dto The query parameters.
        @return The data retrieved from the system.
        """
        ...
``````

# FILE: interfaces/i_session.py

```python
from abc import ABC, abstractmethod
from typing import Any

class ISession(ABC):
    """
    @brief Interface for Database Session.

    @details Provides an abstraction over database ORMs or connections.
    """

    @abstractmethod
    def commit(self) -> None:
        """@brief Commits the current transaction."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """@brief Rolls back the current transaction."""
        ...

    @abstractmethod
    def execute(self, statement: Any, params: Any = None) -> Any:
        """
        @brief Executes a raw statement or query.

        @param statement The query or statement to execute.
        @param params Optional parameters for the query.
        @return The result of the execution.
        """
        ...

    @abstractmethod
    def query(self, *entities: Any) -> Any:
        """
        @brief Queries the database for the given entities.

        @param entities The entities (e.g. models or columns) to query.
        @return A query object.
        """
        ...
``````

# FILE: middleware/logging_middleware.py

```python
from typing import Any, Callable
from src.interfaces import IMiddleware, ILogger, IContainer

class LoggingMiddleware(IMiddleware):
    """
    @brief Middleware used to automatically log before and after executing a Command/Query.

    @details It automatically resolves `ILogger` from the Container. If there is an error retrieving
    the logger, it falls back to using the basic `print` command.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(LoggingMiddleware(container))

    # When app.execute(MyCommand) is called, the following logs will be printed:
    # [LoggingMiddleware] Starting MyCommand
    # ... executes MyCommand logic ...
    # [LoggingMiddleware] Finished MyCommand
    @endcode
    """
    def __init__(self, container: IContainer):
        """
        @brief Constructor.
        @param container The dependency injection container used to resolve the logger.
        """
        self.container = container

    def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, adding logging before and after.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The input data.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        name = cmd_or_query.__class__.__name__

        try:
            logger = self.container.resolve(ILogger)
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
from typing import Any, Callable, Type, Optional
from src.interfaces import IMiddleware

try:
    from pydantic import BaseModel, ValidationError
except ImportError:
    BaseModel = None
    ValidationError = None

class PydanticValidationMiddleware(IMiddleware):
    """
    @brief Middleware used to validate input DTOs using Pydantic models.

    @details Validates the provided DTO against the given Pydantic model class.
    If the DTO is a dictionary, it will be unpacked. If validation fails,
    an exception is raised or logged.

    @par Requirement:
    Requires the `pydantic` package to be installed.

    @par Tutorial / Usage Example:
    @code
    from pydantic import BaseModel

    class MyDTO(BaseModel):
        name: str
        age: int

    app.use_middleware(PydanticValidationMiddleware(MyDTO))
    @endcode
    """
    def __init__(self, model_class: Any) -> None:
        """
        @brief Constructor.
        @param model_class The Pydantic BaseModel class used for validation.
        """
        if BaseModel is None:
            raise ImportError("pydantic is not installed. Please install it using `pip install pydantic`.")
        self.model_class = model_class

    def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Validates the DTO using the provided Pydantic model.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The Data Transfer Object input to validate.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        @exception ValueError if validation fails.
        """
        try:
            if data_transfer_obj is None:
                validated_dto = self.model_class()
            elif isinstance(data_transfer_obj, dict):
                validated_dto = self.model_class(**data_transfer_obj)
            elif isinstance(data_transfer_obj, self.model_class):
                validated_dto = data_transfer_obj
            else:
                # Try to convert object attributes to dict if possible
                dto_dict = data_transfer_obj.__dict__ if hasattr(data_transfer_obj, '__dict__') else {}
                validated_dto = self.model_class(**dto_dict)
            data_transfer_obj = validated_dto
        except ValidationError as e:
            raise ValueError(f"Validation failed for {cmd_or_query.__class__.__name__}: {e}")

        return next_handler()
``````

# FILE: middleware/timing_middleware.py

```python
from typing import Any, Callable
from src.interfaces import IMiddleware
import time

class TimingMiddleware(IMiddleware):
    """
    @brief Middleware used to measure the execution time of a Command or Query.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(TimingMiddleware())

    # The terminal output will show:
    # [TimingMiddleware] ProcessOrderCommand executed in 12.50 ms
    @endcode
    """
    def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, measuring and printing the execution time.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The input data.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        start_time = time.time()
        result = next_handler()
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(f"[TimingMiddleware] {cmd_or_query.__class__.__name__} executed in {duration:.2f} ms")
        return result
``````

# FILE: middleware/validation_middleware.py

```python
from typing import Any, Callable
from src.interfaces import IMiddleware

class ValidationMiddleware(IMiddleware):
    """
    @brief Middleware used to check the validity (Validate) of the input DTO.

    @details This is a basic example. In a real-world application, you can integrate libraries
    like Pydantic or Marshmallow here to validate the DTO before yielding control
    to the Command execution.

    @par Tutorial / Usage Example:
    @code
    app.use_middleware(ValidationMiddleware())

    # If app.execute(MyCommand, input_dto=None) is called, the Middleware will issue a warning.
    @endcode
    """
    def process(self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, validating the input DTO.

        @param cmd_or_query The Command or Query instance being executed.
        @param data_transfer_obj The input data to validate.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        print(f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}")
        if data_transfer_obj is None:
            print("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
``````

# FILE: modules/__init__.py

```python

``````

# FILE: modules/database_module.py

```python
from typing import Optional, Any
from src.base_module import BaseModule
from src.app_kernel import App
from src.interfaces import IConfig, ILogger, ISession

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
    SQLALCHEMY_INSTALLED = True
except ImportError:
    SQLALCHEMY_INSTALLED = False

class SQLAlchemySessionAdapter(ISession):
    """
    @brief Adapter for SQLAlchemy Session.
    """
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

class DatabaseModule(BaseModule):
    """
    @brief Module for setting up the Database connection and Session.

    @details This module reads the `database.url` from the configuration.
    If SQLAlchemy is installed, it creates an engine and registers an `ISession`
    singleton in the container using `scoped_session`.

    @par Requirement:
    Requires the `sqlalchemy` package to be installed.

    @par Alembic Tutorial:
    To use Alembic for database migrations:
    1. Run `alembic init alembic` to create a new alembic directory.
    2. Edit `alembic.ini` and set `sqlalchemy.url` to your database URL.
    3. Edit `alembic/env.py` to import your declarative base and set `target_metadata = Base.metadata`.
    4. Run `alembic revision --autogenerate -m "Initial"` to create a migration.
    5. Run `alembic upgrade head` to apply migrations.
    """

    def register(self, app: App) -> None:
        logger = self._get_logger(app)

        if not SQLALCHEMY_INSTALLED:
            if logger:
                logger.warning("DatabaseModule: sqlalchemy is not installed. Database setup skipped.")
            return

        try:
            config = app.container.resolve(IConfig)
            db_url = config.get("database.url", "sqlite:///:memory:")
        except Exception:
            db_url = "sqlite:///:memory:"
            if logger:
                logger.info("DatabaseModule: IConfig not found or failed to resolve. Using default in-memory SQLite.")

        try:
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)
            Session = scoped_session(session_factory)

            # Create a singleton adapter for the session
            session_adapter = SQLAlchemySessionAdapter(Session)
            app.container.singleton(ISession, session_adapter)

            if logger:
                logger.info(f"DatabaseModule: SQLAlchemy engine created for {db_url} and ISession registered.")
        except Exception as e:
            if logger:
                logger.error(f"DatabaseModule: Failed to initialize database - {e}")

    def boot(self, app: App) -> None:
        pass

    def _get_logger(self, app: App) -> Optional[ILogger]:
        try:
            return app.container.resolve(ILogger)
        except Exception:
            return None
``````

# FILE: modules/health_module.py

```python
from typing import Any, Dict
from src.base_module import BaseModule
from src.app_kernel import App
from src.interfaces import IQuery, IContainer, IEventBus, ISession

class HealthCheckQuery(IQuery):
    """
    @brief Query to perform a health check on the application components.
    """
    def __init__(self, container: IContainer, event_bus: IEventBus):
        self.container = container
        self.event_bus = event_bus

    def execute(self, input_dto: Any = None) -> Dict[str, Any]:
        """
        @brief Executes the health check.
        @return A dictionary containing the health status of various components.
        """
        status = {
            "status": "healthy",
            "components": {
                "container": "ok",
                "event_bus": "ok",
                "database": "unknown"
            }
        }

        # Check Container
        try:
            self.container.resolve(IContainer)
        except Exception as e:
            status["components"]["container"] = f"error: {str(e)}"
            status["status"] = "unhealthy"

        # Check EventBus
        try:
            # We don't necessarily want to emit a real event if it has side effects,
            # but testing if emit is callable is a basic check.
            # Alternatively, test event_bus exists.
            if not hasattr(self.event_bus, 'emit'):
                raise ValueError("event_bus has no emit method")
        except Exception as e:
            status["components"]["event_bus"] = f"error: {str(e)}"
            status["status"] = "unhealthy"

        # Check Database
        try:
            session = self.container.resolve(ISession)
            # Try a simple query
            try:
                # E.g., for SQLAlchemy: execute("SELECT 1")
                # Using the adapter's execute method. The exact string depends on DB.
                # "SELECT 1" is fairly universal.
                from sqlalchemy import text
                session.execute(text("SELECT 1"))
                status["components"]["database"] = "ok"
            except ImportError as e:
                status["components"]["database"] = f"sqlalchemy not installed"
                status["status"] = "unhealthy"
            except Exception as e:
                status["components"]["database"] = f"error executing query: {str(e)}"
                status["status"] = "unhealthy"
        except Exception:
            status["components"]["database"] = "not configured or resolving failed"

        return status

class HealthModule(BaseModule):
    """
    @brief Module for Application Health Checks.

    @details Registers a HealthCheckQuery to allow monitoring systems to check application health.
    """

    def register(self, app: App) -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        app.container.bind('health.check', HealthCheckQuery)

    def boot(self, app: App) -> None:
        """@brief Boots the Health Module."""
        pass
``````

# FILE: modules/logger_module.py

```python
from src.base_module import BaseModule
from src.app_kernel import App
from src.interfaces import ILogger, IConfig
from src.infra.std_logger import StdLogger

class LoggerModule(BaseModule):
    def register(self, app: App) -> None:
        # Check if config is registered in container to pass to StdLogger
        try:
            config = app.container.resolve(IConfig)
        except Exception:
            config = None

        logger_instance = StdLogger(config)
        app.container.singleton(ILogger, logger_instance)

    def boot(self, app: App) -> None:
        pass
``````

# FILE: scaffold.py

```python
import os
import json

def create_project(project_name: str, base_path: str = ".") -> None:
    """
    @brief Scaffolds a new project structure.

    @details Creates the basic directory structure and files for a new project using this framework.
    It generates a directory containing `main.py` as the entry point (Composition Root), a
    `modules` directory for business logic, and a `config.json` file.

    @par Tutorial / Usage Example:
    @code
    # 1. From the terminal, run the command:
    python src/scaffold.py my_awesome_app

    # 2. Navigate into the project directory and run it:
    cd my_awesome_app
    python main.py
    @endcode

    @param project_name The name of the project to create.
    @param base_path The path where the project should be created. Defaults to the current directory.
    """
    project_dir = os.path.join(base_path, project_name)

    # Initialize directories
    for dir_name in ["domain", "application", "infrastructure", "adapters", "modules"]:
        os.makedirs(os.path.join(project_dir, dir_name), exist_ok=True)
        # Mark as python package
        with open(os.path.join(project_dir, dir_name, "__init__.py"), "w") as f:
            pass

    # Initialize basic config file
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump({"app_name": project_name, "version": "1.0.0"}, f, indent=4)

# Create the sample Composition Root (main.py)
    main_py_content = """import sys
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.infra.config_manager import ConfigManager
from src.app_kernel import App
from src.interfaces import IContainer, IEventBus, IConfig

# Framework Modules
from src.modules.logger_module import LoggerModule
from src.modules.database_module import DatabaseModule
from src.modules.health_module import HealthModule

from src.hot_reloader import HotReloader

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Register core ports
    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Setup basic configuration
    config = ConfigManager()
    # Add your configuration sources here (e.g. DotenvSource)
    container.singleton(IConfig, config)

    # Register Built-in Modules
    app.use(LoggerModule())
    app.use(DatabaseModule())
    app.use(HealthModule())

    # Automatically scan and load IModules present in the 'modules' package
    try:
        app.boot(auto_discover="modules")
        print("Application booted successfully.")
    except Exception as e:
        print(f"Error booting application: {e}")

if __name__ == "__main__":
    if "--watch" in sys.argv:
        reloader = HotReloader(["domain", "application", "infrastructure", "adapters", "modules", "main.py"])
        reloader.start()
    main()
"""
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

