from src.core import BaseModule, App, ILogger, IConfig
from src.infra.std_logger import StdLogger

class LoggerModule(BaseModule):
    def register(self, app: App) -> None:
        # Check if config is registered in container to pass to StdLogger
        try:
            config = app.container.resolve(IConfig)
        except Exception:
            config = None

        logger_instance = StdLogger(config)
        app.container.singleton(ILogger, logger_instance)

    def boot(self, app: App) -> None:
        pass
