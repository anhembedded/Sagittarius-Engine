import uuid
from typing import Any, Optional
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken


class BackgroundTask:
    """
    @brief Represents a running background task (sync thread or async future).
    """

    def __init__(self, name: str, token: Optional[CancellationToken] = None) -> None:
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.token: CancellationToken = (
            token if token is not None else CancellationToken()
        )
        self.future: Optional[Any] = None
        self.status: str = "pending"  # pending, running, completed, failed
        self.error: Optional[Exception] = None

    def cancel(self) -> None:
        """
        @brief Signals cooperative cancellation and cancels underlying future.
        """
        self.token.cancel()
        if self.future is not None:
            self.future.cancel()
            self.status = "cancelled"
