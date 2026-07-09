from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel import App

from sagittarius_engine.base import BaseModule
from sagittarius_engine.infrastructure.thread_manager import ThreadManager
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.infrastructure.persistence.i_thread_manager import IThreadManager

class ThreadManagerModule(BaseModule):
    """!
    @brief Module for registering the ThreadManager in the application container.
    """

    def register(self, app: "App") -> None:
        """!
        @brief Register the ThreadManager as a singleton in the dependency container.

        Reads 'thread_manager.max_workers' from IConfig, defaulting to 4,
        and initializes the ThreadManager.

        @param app The App instance containing the dependency container.
        """
        # Resolve IConfig to get max_workers setting
        config: Any = app.container.resolve(IConfig)

        max_workers = 4
        if config:
            max_workers = config.get("thread_manager.max_workers", 4)

        # Ensure max_workers is an int (config might return a string depending on source)
        try:
            max_workers = int(max_workers)
        except (ValueError, TypeError):
            max_workers = 4

        thread_manager = ThreadManager(max_workers=max_workers)
        app.container.singleton(IThreadManager, thread_manager)
