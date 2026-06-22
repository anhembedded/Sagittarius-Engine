import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class Event:
    """
    Base class for all domain events to provide common identification and timing.
    Ensures every event has a unique ID and a timestamp of when it occurred.
    """
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
