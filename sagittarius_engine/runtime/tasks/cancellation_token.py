import threading


class CancellationToken:
    """
    @brief Thread-safe cooperative cancellation token using threading.Event.
    """

    def __init__(self, event: threading.Event = None) -> None:
        self._event = event if event is not None else threading.Event()

    def is_cancelled(self) -> bool:
        """
        @brief Returns True if cancellation has been requested.
        """
        return self._event.is_set()

    @property
    def is_cancellation_requested(self) -> bool:
        """
        @brief Returns True if cancellation has been requested (alternate property).
        """
        return self._event.is_set()

    def cancel(self) -> None:
        """
        @brief Triggers the cancellation event.
        """
        self._event.set()

    def wait(self, timeout: float = None) -> bool:
        """
        @brief Blocks until the token is cancelled or the timeout expires.
        @return True if the token was cancelled, False if the timeout expired.
        """
        return self._event.wait(timeout)
