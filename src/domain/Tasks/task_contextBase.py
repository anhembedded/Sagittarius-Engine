from abc import ABC, abstractmethod


class ITaskContext(ABC):
    """Abstraction layer between a running Task and its runtime (Qt / CLI).

    This is a full ABC — every adapter MUST implement all methods.
    """

    @abstractmethod
    def report_progress(self, value: int) -> None:
        """Report a progress percentage (0–100)."""

    @abstractmethod
    def report_message(self, message: str) -> None:
        """Report a human-readable status message."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Emit a diagnostic log entry (does NOT mix with UI messages)."""

    @abstractmethod
    def is_cancelled(self) -> bool:
        """Return True if the task has been requested to cancel."""

    @abstractmethod
    def cancel(self) -> None:
        """Request cancellation. Called externally (e.g. by TimeoutWrapper)."""
