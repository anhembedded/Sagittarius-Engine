from typing import Any
from src.domain.logger import Logger
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger



class LoguruLoggerAdapter(Logger):
    """
    Adapter pattern to translate Logger domain interface to Loguru infrastructure.
    # Adapter Pattern
    """

    def __init__(self, infra_logger: LoguruLogger) -> None:
        self._infra = infra_logger

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.debug(message, *args, depth=2, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.info(message, *args, depth=2, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.warning(message, *args, depth=2, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.error(message, *args, depth=2, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.exception(message, *args, depth=2, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.critical(message, *args, depth=2, **kwargs)
