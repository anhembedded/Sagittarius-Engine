from typing import Any, Optional
from sagittarius_engine.kernel.module_loader import ModuleLoader
from sagittarius_engine.interfaces import ILogger

class Bootstrap:
    """Responsible for bootstrapping the engine."""

    def __init__(self, app: Any) -> None:
        self.app = app
        self.module_loader = ModuleLoader(app)

    def _get_logger(self) -> ILogger | None:
        try:
            from sagittarius_engine.interfaces import ILogger
            return self.app.container.resolve(ILogger)
        except Exception:
            return None

    def boot(self, auto_discover: Optional[str] = None) -> None:
        """
        @brief Boots the application.
        """
        logger = self._get_logger()
        if logger:
            logger.info("App is booting...")

        self.app.lifecycle.set_booting()

        if auto_discover:
            self.module_loader.discover_and_load(auto_discover)

        for module in self.app.modules:
            module.boot(self.app)

        self.app.lifecycle.set_booted()

        if logger:
            logger.info(f"App booted successfully with {len(self.app.modules)} modules.")

        self.app.event_bus.emit("app.booted", self.app)
