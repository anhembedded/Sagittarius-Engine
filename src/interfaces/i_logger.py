from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class ILogger(ABC):
    """
    @brief Interface for the Logging system.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        """@brief Logs an informational message."""
        ...

    @abstractmethod
    def warning(self, message: str) -> None:
        """@brief Logs a warning message."""
        ...

    @abstractmethod
    def error(self, message: str) -> None:
        """@brief Logs an error message."""
        ...

    @abstractmethod
    def debug(self, message: str) -> None:
        """@brief Logs a debug message."""
        ...
