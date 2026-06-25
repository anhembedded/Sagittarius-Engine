# PROJECT CONTEXT

**Root:** `/home/hoanganh/Documents/Sagittarius_ForkBoy/src/`
**Pattern:** `*py`
**Files:** 29
**Generated:** 2026-06-24 17:03:26

## Directory Tree

```
src
├── __init__.py
├── app_kernel.py
├── base_event.py
├── base_module.py
├── exceptions.py
├── infra
│   ├── asyncio_event_bus.py
│   ├── config_manager.py
│   ├── dict_config.py
│   ├── memory_event_bus.py
│   ├── resilient_event_bus.py
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
│   ├── i_logger.py
│   ├── i_middleware.py
│   ├── i_module.py
│   └── i_query.py
├── middleware
│   ├── logging_middleware.py
│   ├── timing_middleware.py
│   └── validation_middleware.py
├── modules
│   ├── __init__.py
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

    def execute(self, cmd_or_query: Any, dto: Any, final_handler: Callable[[], Any]) -> Any:
        """
        @brief Executes the entire Middleware chain.

        @param cmd_or_query The Command or Query instance.
        @param dto The Data Transfer Object input.
        @param final_handler The final execution handler for the Command/Query.
        @return The final execution result.
        """

        def build_chain(index: int) -> Callable[[], Any]:
            if index < len(self.middlewares):
                middleware = self.middlewares[index]
                next_handler = build_chain(index + 1)
                return lambda: middleware.process(cmd_or_query, dto, next_handler)
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
        except ImportError:
            return
        if not hasattr(package, '__path__'):
            return
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f'{modules_package}.{name}'
            sub_package = importlib.import_module(full_module_name)
            for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                if issubclass(obj, IModule) and obj is not IModule and (obj is not BaseModule):
                    app.use(obj())

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
            data = source.read()
            self._cache.update(data)
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
            handler(data)

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
                raise DependencyResolutionError(f"Failed to resolve '{name}' for {concrete.__name__}: {str(e)}")

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

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error executing handler for event {event_name}: {e}")

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
from .i_command import ICommand
from .i_query import IQuery
from .i_module import IModule
from .i_event_bus import IEventBus
from .i_async_event_bus import IAsyncEventBus
from .i_container import IContainer
from .i_middleware import IMiddleware
from .i_logger import ILogger
from .i_config import IConfig

__all__ = ['ICommand', 'IQuery', 'IModule', 'IEventBus', 'IContainer', 'IMiddleware', 'ILogger', 'IConfig']
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
        def process(self, cmd_or_query, dto, next_handler):
            print("Before executing the command")
            result = next_handler()  # Calls the next handler or the main command
            print("After executing the command")
            return result
    @endcode
    """

    @abstractmethod
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The Data Transfer Object input.
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

    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, adding logging before and after.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The input data.
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
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, measuring and printing the execution time.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The input data.
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
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        """
        @brief Processes the command or query, validating the input DTO.

        @param cmd_or_query The Command or Query instance being executed.
        @param dto The input data to validate.
        @param next_handler The next middleware or the final execution function.
        @return The result of the operation.
        """
        print(f"[ValidationMiddleware] Validating DTO for {cmd_or_query.__class__.__name__}")
        if dto is None:
            print("[ValidationMiddleware] Warning: DTO is None!")
        return next_handler()
``````

# FILE: modules/__init__.py

```python

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

    # Initialize directory
    os.makedirs(os.path.join(project_dir, "modules"), exist_ok=True)

    # Initialize basic config file
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump({"app_name": project_name, "version": "1.0.0"}, f, indent=4)

    # Mark the modules directory as a Python package
    with open(os.path.join(project_dir, "modules", "__init__.py"), "w") as f:
        pass

    # Create the sample Composition Root (main.py)
    main_py_content = """from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.app_kernel import App
from src.interfaces import IContainer, IEventBus

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Automatically scan and load IModules present in the 'modules' package
    try:
        app.boot(auto_discover="modules")
        print("Application booted successfully.")
    except Exception as e:
        print(f"Error booting application: {e}")

if __name__ == "__main__":
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

