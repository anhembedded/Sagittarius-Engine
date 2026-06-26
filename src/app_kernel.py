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
    def discover(modules_package_str_path: str, app: 'App') -> None:
        """
        @brief Scans the specified package and loads the IModules.

        @param modules_package The string path to the modules package.
        @param app The current application instance.
        """
        try:
            package = importlib.import_module(modules_package_str_path)
        except ImportError as e:
            logger = app._get_logger()
            if logger:
                logger.warning(f"Could not discover package {modules_package_str_path}: {e}")
            return
        if not hasattr(package, '__path__'):
            return
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f'{modules_package_str_path}.{name}'
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
