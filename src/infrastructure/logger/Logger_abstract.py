from abc import ABC, abstractmethod
from typing import Any

class LoggerAbstract_infr(ABC):
    """
    Abstract base class for Logger. Defines the interface for logging methods.
    # Abstract Base Class
    """
    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass