from typing import Any
from sagittarius_engine.exceptions import ModuleRegistrationError
from sagittarius_engine.kernel.middleware_pipeline import MiddlewarePipeline
from sagittarius_engine.kernel.lifecycle import EngineLifecycle
from sagittarius_engine.kernel.bootstrap import Bootstrap
from sagittarius_engine.kernel.dispatcher import Dispatcher
from sagittarius_engine.interfaces import (
    ICommand,
    IContainer,
    IEventBus,
    ILogger,
    IMiddleware,
    IModule,
    IQuery,
    IConfig,
)


class EngineServices:
    """Registry for core engine services (Phase 2.5)."""

    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        self._container = container
        self._event_bus = event_bus

    @property
    def container(self) -> IContainer:
        return self._container

    @property
    def event_bus(self) -> IEventBus:
        return self._event_bus

    @property
    def logger(self) -> ILogger | None:
        try:
            return self._container.resolve(ILogger)
        except Exception:
            return None

    @property
    def config(self) -> IConfig | None:
        try:
            return self._container.resolve(IConfig)
        except Exception:
            return None


class App:
    """
    @brief The public façade of the Sagittarius Engine.

    @details App coordinates core services (Container, EventBus) and delegates
    logic to dedicated components (Bootstrap, Dispatcher, EngineLifecycle).
    """

    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        """
        @brief Initializes the application with the core ports.

        @param container The dependency injection container.
        @param event_bus The event bus.
        """
        self.services = EngineServices(container, event_bus)
        self.modules: list[IModule] = []
        self.pipeline = MiddlewarePipeline()

        # Kernel services
        self.lifecycle = EngineLifecycle()
        self.bootstrap = Bootstrap(self)
        self.dispatcher = Dispatcher(self)

    @property
    def container(self) -> IContainer:
        return self.services.container

    @property
    def event_bus(self) -> IEventBus:
        return self.services.event_bus

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

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        """
        @brief Registers a Middleware for the application.
        @param middleware_instance The middleware instance.
        """
        self.pipeline.add(middleware_instance)

    def _get_logger(self) -> ILogger | None:
        return self.services.logger

    def boot(self, auto_discover: str | None = None) -> None:
        """
        @brief Boots the application.
        """
        self.bootstrap.boot(auto_discover)

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        """
        @brief Executes a Command through the Middleware Pipeline.
        """
        return self.dispatcher.execute(command_class, input_dto)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        """
        @brief Executes a Query through the Middleware Pipeline.
        """
        return self.dispatcher.query(query_class, input_dto)
