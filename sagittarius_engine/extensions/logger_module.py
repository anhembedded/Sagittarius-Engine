from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.interfaces import IConfig, ILogger
from sagittarius_engine.interfaces.i_extension import IExtension


class LoggerExtension(IExtension):
    """
    @brief Extension for Logger setup.
    """

    def register(self, context: "EngineContext") -> None:
        try:
            config: IConfig = context.container.resolve(IConfig)
        except Exception:
            config = None  # type: ignore[assignment]

        logger_instance = StdLogger(config)
        context.container.singleton(ILogger, logger_instance)

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass


class LoggerModule(LoggerExtension):
    """
    @brief Deprecated wrapper for LoggerExtension.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "LoggerModule is deprecated. Use LoggerExtension instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
