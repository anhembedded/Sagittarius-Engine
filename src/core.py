from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional
import inspect
import pkgutil
import importlib

T = TypeVar('T')

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
    def emit(self, event_name: str, data: Any = None) -> None:
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

class IConfig(ABC):
    """
    @brief Interface for Configuration management.
    """
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
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

class ModuleRegistrationError(Exception):
    """@brief Error raised when a module fails to register."""
    pass

class DependencyResolutionError(Exception):
    """@brief Error raised when the Container fails to resolve a dependency."""
    pass

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
            full_module_name = f"{modules_package}.{name}"
            sub_package = importlib.import_module(full_module_name)

            for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                if issubclass(obj, IModule) and obj is not IModule and obj is not BaseModule:
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
            raise ModuleRegistrationError("Module must implement IModule")
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

    def boot(self, auto_discover: Optional[str] = None) -> None:
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
            logger.info("App is booting...")

        if auto_discover:
            ModuleAutoDiscovery.discover(auto_discover, self)
        for module in self.modules:
            module.boot(self)

        if logger:
            logger.info(f"App booted successfully with {len(self.modules)} modules.")

        self.event_bus.emit('app.booted', self)

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
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
            logger.info(f"Executing command: {command_class.__name__}")

        command = self.container.resolve(command_class)
        def final() -> Any:
            return command.execute(input_dto)
        return self.pipeline.execute(command, input_dto, final)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        """
        @brief Executes a Query through the Middleware Pipeline.

        @details Works similarly to `execute` but is intended for data retrieval operations.

        @param query_class The class type of the query to execute.
        @param input_dto The input data.
        @return The execution result.
        """
        logger = self._get_logger()
        if logger:
            logger.info(f"Executing query: {query_class.__name__}")

        query = self.container.resolve(query_class)
        def final() -> Any:
            return query.execute(input_dto)
        return self.pipeline.execute(query, input_dto, final)
