from abc import ABC, abstractmethod
from datetime import datetime

class IDomainEvent(ABC):
    """
    @brief Interface for domain events in the application.

    @details Mandates the presence of an event_id and occurred_on timestamp for all events.
    """

    @property
    @abstractmethod
    def event_id(self) -> str:
        """
        @brief The unique identifier of the event.
        """
        pass

    @property
    @abstractmethod
    def occurred_on(self) -> datetime:
        """
        @brief The timestamp when the event occurred.
        """
        pass
