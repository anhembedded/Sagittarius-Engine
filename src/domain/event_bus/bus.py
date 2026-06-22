from abc import ABC, abstractmethod
from typing import Type, TypeVar, Callable, Awaitable, Union

from .event import Event

T = TypeVar("T", bound=Event)

# Type hint for event handlers (can be synchronous or asynchronous)
EventHandler = Union[
    Callable[[T], None],
    Callable[[T], Awaitable[None]],
]


class EventBus(ABC):
    """
    Interface for the domain event bus to decouple event publishers from subscribers.
    Provides a mechanism to subscribe to, unsubscribe from, and publish domain events.
    """

    @abstractmethod
    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Registers a handler for a specific event type to receive future publications.
        Why: Allows components to react to domain events without direct coupling to publishers.
        """
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Removes a previously registered handler for an event type.
        Why: Enables dynamic management of event subscriptions and prevents memory leaks.
        """
        pass

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """
        Distributes a domain event to all its registered handlers.
        Why: Propagates state changes or significant occurrences across the system.
        """
        pass
