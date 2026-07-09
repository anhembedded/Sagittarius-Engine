from sagittarius_engine.kernel import App
from sagittarius_engine.base import BaseModule
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.interfaces import IConfig, ILogger


class LoggerModule(BaseModule):
    def register(self, app: App) -> None:
        # Check if config is registered in container to pass to StdLogger
        try:
            config: IConfig = app.container.resolve(IConfig)
        except Exception:
            config = None  # type: ignore[assignment]

        logger_instance = StdLogger(config)
        app.container.singleton(ILogger, logger_instance)

    def boot(self, app: App) -> None:
        pass
