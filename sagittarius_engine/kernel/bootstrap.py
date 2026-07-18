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

        # Start Async Runtime early so extensions/hosted services can use it
        self.context.async_runtime.start()

        try:
            if auto_discover:
                self.context.module_loader.discover_and_load(auto_discover)

            self.context.extension_manager.initialize_and_start()

            # Start Hosted Services
            self.context.hosted_services.start()

            # Start Scheduler
            self.context.scheduler.start()

        except Exception as e:
            if logger:
                logger.error(
                    f"Error during boot sequence: {e}. Shutting down runtime..."
                )
            # Clean up what was started
            try:
                self.context.scheduler.stop()
            except Exception:
                pass
            try:
                self.context.hosted_services.stop()
            except Exception:
                pass
            try:
                self.context.async_runtime.stop()
            except Exception:
                pass
            raise e

        self.context.lifecycle.set_booted()

        if logger:
            logger.info(
                f"App booted successfully with {len(self.context.modules)} modules."
            )

        self.context.event_bus.emit("app.booted", self.context.app)
