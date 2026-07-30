from dataclasses import dataclass


@dataclass
class ExtensionInitializing:
    """Event emitted when an extension is about to initialize."""

    extension_name: str


@dataclass
class ExtensionStarted:
    """Event emitted when an extension has started."""

    extension_name: str


@dataclass
class ExtensionStopped:
    """Event emitted when an extension has stopped."""

    extension_name: str


@dataclass
class ExtensionDisposed:
    """Event emitted when an extension has been disposed."""

    extension_name: str


@dataclass
class HostedServiceStarted:
    """Event emitted when a hosted service has started."""

    service_name: str


@dataclass
class HostedServiceStopped:
    """Event emitted when a hosted service has stopped."""

    service_name: str


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


@dataclass
class SchedulerStarted:
    """Event emitted when the scheduler has started."""


@dataclass
class SchedulerStopped:
    """Event emitted when the scheduler has stopped."""
