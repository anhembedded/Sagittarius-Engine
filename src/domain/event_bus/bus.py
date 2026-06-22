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
    Abstract interface for the Domain Event Bus.
    Decouples the generation of domain events from their consumers.
    """

    @abstractmethod
    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Subscribe a handler to a specific event type.

        Args:
            event_type: The class of the event to subscribe to.
            handler: A callable (sync function or async coroutine) to execute on event.
        """
        pass

    @abstractmethod
    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Unsubscribe a handler from a specific event type.

        Args:
            event_type: The class of the event to unsubscribe from.
            handler: The previously subscribed callable.
        """
        pass

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """
        Publish an event to all interested handlers.

        Args:
            event: The event instance to publish.
        """
        pass
