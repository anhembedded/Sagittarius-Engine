from typing import Any, Protocol
from src.domain.logger.Logger_api import Logger

class LoggerInfraPort(Protocol):
    def debug(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...
    def info(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...
    def warning(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...
    def error(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...
    def exception(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...
    def critical(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None: ...

class Logger_Adapter(Logger):
    """
    Adapter pattern to translate Logger domain interface to infrastructure.
    # Adapter Pattern
    """

    def __init__(self, infra_logger: LoggerInfraPort) -> None:
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