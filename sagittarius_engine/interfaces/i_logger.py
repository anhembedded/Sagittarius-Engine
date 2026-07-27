from abc import ABC, abstractmethod
from typing import Any


class ILogger(ABC):
    """
    @brief Interface for the Logging system supporting structured metadata.
    """

    @abstractmethod
    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs an informational message."""
        ...

    @abstractmethod
    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs a warning message."""
        ...

    @abstractmethod
    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs an error message."""
        ...

    @abstractmethod
    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs a debug message."""
        ...
