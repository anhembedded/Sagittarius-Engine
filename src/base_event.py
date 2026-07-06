import uuid
from datetime import UTC, datetime

from .interfaces import IDomainEvent


class BaseEvent(IDomainEvent):
    """
    @brief Base class for domain events, providing an ID and a timestamp.

    @details This class is meant to be subclassed by specific event classes to provide
    a standard set of metadata. However, there's no strict requirement to inherit from
    it; it serves as a utility.
    """

    def __init__(self) -> None:
        self._event_id: str = str(uuid.uuid4())
        self._occurred_on: datetime = datetime.now(UTC)

    @property
    def event_id(self) -> str:
        return self._event_id

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

    def to_dict(self) -> dict:
        """
        @brief Returns a dictionary representation of the event.
        """
        data = self.__dict__.copy()
        if "_event_id" in data:
            data["event_id"] = data.pop("_event_id")
        if "_occurred_on" in data:
            data["occurred_on"] = data.pop("_occurred_on")

        data["occurred_on"] = self.occurred_on.isoformat()
        return data
