from enum import Enum
import uuid
from typing import Any, Optional, Callable
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
from datetime import datetime, timezone


from sagittarius_engine.interfaces.i_task_manager import ITaskHandle


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BackgroundTask(ITaskHandle):
    """
    @brief Represents a running background task (sync thread or async future).
    """

    def __init__(
        self,
        name: str,
        token: Optional[CancellationToken] = None,
        critical: bool = False,
        on_progress_update: Optional[Callable[[float, str], None]] = None,
    ) -> None:
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self.critical: bool = critical
        self._token: CancellationToken = (
            token if token is not None else CancellationToken()
        )
        self._future: Optional[Any] = None
        self._status: TaskState = TaskState.PENDING
        self._progress: float = 0.0
        self._on_progress_update: Optional[Callable[[float, str], None]] = (
            on_progress_update
        )
        self.error: Optional[Exception] = None
        self.start_time: Optional[datetime] = datetime.now(timezone.utc)
        self.end_time: Optional[datetime] = None

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
    def status(self) -> TaskState:
        return self._status

    @status.setter
    def status(self, value: TaskState) -> None:
        self._status = value
        if value in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED):
            self.end_time = datetime.now(timezone.utc)

    @property
    def progress(self) -> float:
        return self._progress

    def update_progress(self, value: float, message: str = "") -> None:
        """
        @brief Updates the task's progress (0.0 to 100.0) and emits an event if configured.
        """
        if not (0.0 <= value <= 100.0):
            raise ValueError("Progress must be between 0.0 and 100.0")
        self._progress = value
        if self._on_progress_update:
            self._on_progress_update(value, message)

    def cancel(self) -> None:
        """
        @brief Signals cooperative cancellation and cancels underlying future.
        """
        self.token.cancel()
        if self.future is not None:
            self.future.cancel()  # type: ignore
            self.status = TaskState.CANCELLED
