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
    """
    @brief The public façade of the Sagittarius Engine.

    @details App delegates runtime operations to EngineContext.
    """

    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        """
        @brief Initializes the application with the core ports.

        @param container The dependency injection container.
        @param event_bus The event bus.
        """
        self.context = EngineContext(self, container, event_bus)

    @property
    def container(self) -> IContainer:
        return self.context.container

    @property
    def event_bus(self) -> IEventBus:
        return self.context.event_bus

    @property
    def modules(self) -> list[IModule]:
        return self.context.modules

    @property
    def pipeline(self) -> Any:
        return self.context.middleware_pipeline

    @property
    def lifecycle(self) -> Any:
        return self.context.lifecycle

    def use(self, module: IModule) -> None:
        """
        @brief Manually adds a Module to the App and calls its `register` method immediately.

        @param module The module instance to add.
        @exception ModuleRegistrationError If the module does not implement IModule.
        """
        if not isinstance(module, IModule):
            raise ModuleRegistrationError("Module must implement IModule")
        self.context.modules.append(module)
        module.register(self)

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        """
        @brief Registers a Middleware for the application.
        @param middleware_instance The middleware instance.
        """
        self.context.middleware_pipeline.add(middleware_instance)

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def boot(self, auto_discover: str | None = None) -> None:
        """
        @brief Boots the application.
        """
        self.context.bootstrap.boot(auto_discover)

    def execute(self, command_class: type[ICommand], input_dto: Any = None) -> Any:
        """
        @brief Executes a Command through the Middleware Pipeline.
        """
        return self.context.dispatcher.execute(command_class, input_dto)

    def query(self, query_class: type[IQuery], input_dto: Any = None) -> Any:
        """
        @brief Executes a Query through the Middleware Pipeline.
        """
        return self.context.dispatcher.query(query_class, input_dto)
