from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.thread_manager import ThreadManager
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.interfaces.i_thread_manager import (
    IThreadManager,
)


class ThreadManagerExtension(IExtension):
    """
    @brief Extension for ThreadManager setup.
    """

    def register(self, context: "EngineContext") -> None:
        # Resolve IConfig to get max_workers setting
        config: Any = context.container.resolve(IConfig)

        max_workers = 4
        if config:
            max_workers = config.get("thread_manager.max_workers", 4)

        try:
            max_workers = int(max_workers)
        except (ValueError, TypeError):
            max_workers = 4

        thread_manager = ThreadManager(max_workers=max_workers)
        context.container.singleton(IThreadManager, thread_manager)

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass

from sagittarius_engine.interfaces.i_module import IModule
from sagittarius_engine.interfaces.i_engine_context import IEngineContext

class ThreadManagerModule(IModule):
    def register(self, context: IEngineContext) -> None:
        pass

    def boot(self, app) -> None:
        pass
