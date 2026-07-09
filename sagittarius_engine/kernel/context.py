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


class EngineContext:
    """The runtime composition root of the Sagittarius Engine.

    It owns every engine service and coordinates communication between engine subsystems.
    It does not contain application or business logic.
    """

    def __init__(self, app: Any, container: IContainer, event_bus: IEventBus) -> None:
        self.app = app
        self.container = container
        self.event_bus = event_bus
        self.middleware_pipeline = MiddlewarePipeline()
        self.modules: list[IModule] = []

        # Instantiating subsystems with shared EngineContext
        self.lifecycle = EngineLifecycle(self)
        self.module_loader = ModuleLoader(self)
        self.bootstrap = Bootstrap(self)
        self.dispatcher = Dispatcher(self)

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
