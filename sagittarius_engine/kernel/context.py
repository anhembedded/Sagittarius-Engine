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
    """The runtime composition root of the Sagittarius Engine.

    It owns every engine service and coordinates communication between engine subsystems.
    It does not contain application or business logic.
    """

    def __init__(self, app: Any, container: IContainer, event_bus: IEventBus) -> None:
        self.app = app
        self.container = container
        self.event_bus = event_bus
        self.middleware_pipeline = MiddlewarePipeline()
        self.extension_manager = ExtensionManager(self)

        # Instantiating subsystems with shared EngineContext
        self.lifecycle = EngineLifecycle(self)
        self.module_loader = ModuleLoader(self)
        self.bootstrap = Bootstrap(self)
        self.dispatcher = Dispatcher(self)

        # Runtime Infrastructure
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

        # Register runtime in container as singletons
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
