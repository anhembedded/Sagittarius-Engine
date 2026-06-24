import uuid
from datetime import datetime, timezone

class BaseEvent:
    """
    @brief Base class for domain events, providing an ID and a timestamp.

    @details This class is meant to be subclassed by specific event classes to provide
    a standard set of metadata. However, there's no strict requirement to inherit from
    it; it serves as a utility.
    """
    def __init__(self) -> None:
        self.event_id: str = str(uuid.uuid4())
        self.occurred_on: datetime = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """
        @brief Returns a dictionary representation of the event.
        """
        data = self.__dict__.copy()
        data['occurred_on'] = self.occurred_on.isoformat()
        return data
