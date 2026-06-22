import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Type, TypeVar, Callable, Union

@dataclass(frozen=True)
class Event:
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

T = TypeVar("T", bound=Event)

EventHandler = Callable[[T], None]

class EventBus(ABC):
    @abstractmethod
    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        ...

    @abstractmethod
    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        ...

    @abstractmethod
    def publish(self, event: Event) -> None:
        ...
