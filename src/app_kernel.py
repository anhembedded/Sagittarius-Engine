from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional, List
import inspect
import pkgutil
import importlib

from src.interfaces import IModule, IContainer, IEventBus, IMiddleware, ICommand, IQuery, ILogger
from src.exceptions import ModuleRegistrationError, DependencyResolutionError
from src.base_module import BaseModule

class MiddlewarePipeline:
    """
    Manages a chain of Middlewares using the Onion execution pattern:
    - Requests flow inward through each middleware until they reach the core handler.
    - Results flow outward back through the middleware chain.
    """

    def __init__(self) -> None:
        # Holds the list of middleware instances in execution order
        self.middlewares: List[IMiddleware] = []

    def add(self, middleware: IMiddleware) -> None:
        """Append a middleware to the end of the chain."""
        self.middlewares.append(middleware)

    def execute(
        self,
        cmd_or_query: Any,
        dto: Any,
        final_handler: Callable[[], Any]
    ) -> Any:
        """
        Execute the entire middleware chain.

        Args:
            cmd_or_query: The Command or Query instance.
            dto: The Data Transfer Object input.
            final_handler: The final execution handler for the Command/Query.

        Returns:
            The final execution result after passing through the pipeline.
        """
        return self.__build_chain(cmd_or_query, dto, final_handler, 0)()

    def __build_chain(
        self,
        cmd_or_query: Any,
        dto: Any,
        final_handler: Callable[[], Any],
        index: int
    ) -> Callable[[], Any]:
        """
        Private helper method to recursively build the middleware chain.
        Each middleware wraps around the next one until the final handler.
        """
        if index >= len(self.middlewares):
            return final_handler

        middleware = self.middlewares[index]
        # Instead of defining a nested handler, delegate to another private method
        return lambda: self.__invoke_middleware(
            middleware, cmd_or_query, dto, final_handler, index
        )

    def __invoke_middleware(
        self,
        middleware: IMiddleware,
        cmd_or_query: Any,
        dto: Any,
        final_handler: Callable[[], Any],
        index: int
    ) -> Any:
        """
        Invoke a single middleware and pass control to the next one.
        """
        return middleware.process(
            cmd_or_query,
            dto,
            self.__build_chain(cmd_or_query, dto, final_handler, index + 1)
        )

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

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        """
        @brief Registers a Middleware for the application.
        @param middleware The middleware instance.
        """
        self.pipeline.add(middleware_instance)

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
        command = self.container.resolve(command_class) # type: ignore[var-annotated]

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
        query = self.container.resolve(query_class) # type: ignore[var-annotated]

        def final() -> Any:
            return query.execute(input_dto)
        return self.pipeline.execute(query, input_dto, final)
