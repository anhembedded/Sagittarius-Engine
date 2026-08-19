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

    @abstractmethod
    def critical(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs a critical message — the standard Python `logging`
        level above ERROR, for a failure that threatens the whole process
        rather than one operation."""
        ...

    @abstractmethod
    def trace(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """@brief Logs a trace message — one level below DEBUG (not a
        standard Python `logging` level; registered by `StdLogger`), for
        detail too high-frequency even for a normal `--dev` run (e.g.
        per-frame/per-pixel). Only emitted when `log.level=TRACE`, which
        `--debug` sets (`--dev` alone still stops at DEBUG)."""
        ...
