from typing import Any
from sagittarius_engine.exceptions import DependencyResolutionError, ModuleRegistrationError
from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
from sagittarius_engine.kernel.module_auto_discovery import ModuleAutoDiscovery
from sagittarius_engine.interfaces import ICommand, IContainer, IEventBus, ILogger, IMiddleware, IModule, IQuery

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
    app.boot(auto_discover="sagittarius_engine.extensions")

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

    def _get_logger(self) -> ILogger | None:
        try:
            return self.container.resolve(ILogger)
        except DependencyResolutionError:
            return None

    def boot(self, auto_discover: str | None=None) -> None:
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
        command = self.container.resolve(command_class)  # type: ignore[var-annotated]

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
        query = self.container.resolve(query_class)  # type: ignore[var-annotated]

        def final() -> Any:
            return query.execute(input_dto)
        return self.pipeline.execute(query, input_dto, final)
