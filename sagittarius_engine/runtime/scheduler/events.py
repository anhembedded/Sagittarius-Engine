from dataclasses import dataclass


@dataclass
class SchedulerStarted:
    """Event emitted when the scheduler has started."""


@dataclass
class SchedulerStopped:
    """Event emitted when the scheduler has stopped."""
