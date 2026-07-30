from dataclasses import dataclass


@dataclass
class TaskStarted:
    """Event emitted when a background task has started."""
    event_name = "runtime.tasks.started"
    task_id: str
    task_name: str


@dataclass
class TaskCompleted:
    """Event emitted when a background task has completed successfully."""
    event_name = "runtime.tasks.completed"
    task_id: str
    task_name: str


@dataclass
class TaskProgressUpdated:
    """Event emitted when a background task updates its progress."""
    event_name = "runtime.tasks.progress"
    task_id: str
    progress: float
    message: str


@dataclass
class TaskFailed:
    """Event emitted when a background task has failed."""
    event_name = "runtime.tasks.failed"
    task_id: str
    task_name: str
    error: Exception
