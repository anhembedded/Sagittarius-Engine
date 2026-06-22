from abc import ABC, abstractmethod
from typing import Any

class Logger(ABC):
    """
    Core Domain Logger Interface. All methods accept standard message template
    with optional formatting (*args, **kwargs).
    """

    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: ...

