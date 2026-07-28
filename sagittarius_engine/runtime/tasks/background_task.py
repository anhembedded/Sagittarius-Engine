import uuid
from typing import Any, Optional
from sagittarius_engine.interfaces.i_task_manager import ITaskHandle
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken


class BackgroundTask(ITaskHandle):
    """
    @brief Represents a running background task (sync thread or async future).
    """

    def __init__(
        self,
        name: str,
        token: Optional[CancellationToken] = None,
        critical: bool = False,
    ) -> None:
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self.critical: bool = critical
        self._token: CancellationToken = (
            token if token is not None else CancellationToken()
        )
        self._future: Optional[Any] = None
        self._status: str = "pending"  # pending, running, completed, failed
        self.error: Optional[Exception] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def token(self) -> CancellationToken:
        return self._token

    @token.setter
    def token(self, value: CancellationToken) -> None:
        self._token = value

    @property
    def future(self) -> Optional[Any]:
        return self._future

    @future.setter
    def future(self, value: Optional[Any]) -> None:
        self._future = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    def cancel(self) -> None:
        """
        @brief Signals cooperative cancellation and cancels underlying future.
        """
        self.token.cancel()
        if self.future is not None:
            self.future.cancel()
            self.status = "cancelled"
