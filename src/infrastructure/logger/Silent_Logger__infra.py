from typing import Any
from src.domain.logger import Logger

class SilentLoggerAdapter(Logger):
    """
    Adapter pattern implementing Logger domain interface as a no-op silent logger.
    # Adapter Pattern
    """

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass
