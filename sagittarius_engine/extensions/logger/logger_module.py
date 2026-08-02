from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.interfaces import IConfig, ILogger


class LoggerExtension(IExtension):
    """
    @brief Extension for Logger setup.
    """

    def register(self, context: "IEngineContext") -> None:
        try:
            config: IConfig = context.container.resolve(IConfig)
        except Exception:
            config = None  # type: ignore[assignment]

        logger_instance = StdLogger(config)
        context.container.singleton(ILogger, logger_instance)

    def boot(self, context: "IEngineContext") -> None:
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        pass
