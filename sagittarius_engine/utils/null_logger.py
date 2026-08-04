from typing import Any
from sagittarius_engine.interfaces.i_logger import ILogger

class NullLogger(ILogger):
    """A dummy logger that safely ignores all log messages."""

    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        pass
