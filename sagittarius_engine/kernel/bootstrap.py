from typing import Any, Optional
from sagittarius_engine.interfaces import ILogger


class Bootstrap:
    """Responsible for bootstrapping the engine."""

    def __init__(self, context: Any) -> None:
        self.context = context

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def boot(self, auto_discover: Optional[str] = None) -> None:
        """
        @brief Boots the application.
        """
        logger = self._get_logger()
        if logger:
            logger.info("App is booting...")

        self.context.lifecycle.set_booting()

        if auto_discover:
            self.context.module_loader.discover_and_load(auto_discover)

        for module in self.context.modules:
            from sagittarius_engine.interfaces.i_extension import IExtension

            if isinstance(module, IExtension):
                module.boot(self.context)
            else:
                module.boot(self.context.app)

        self.context.lifecycle.set_booted()

        if logger:
            logger.info(
                f"App booted successfully with {len(self.context.modules)} modules."
            )

        self.context.event_bus.emit("app.booted", self.context.app)
