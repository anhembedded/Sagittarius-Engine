from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    """
    Abstract interface for logging in the application.
    Enforces layer boundary separation by keeping external logging library
    dependencies (like Loguru) completely out of the core domain layer.
    """

    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with DEBUG level.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with INFO level.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with WARNING level.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with ERROR level.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass

    @abstractmethod
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with ERROR level including the current traceback.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with CRITICAL level.

        Args:
            message: The log message template.
            *args: Positional arguments for formatting.
            **kwargs: Keyword arguments for formatting.
        """
        pass
