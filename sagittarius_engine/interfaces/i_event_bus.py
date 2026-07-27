from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

from sagittarius_engine.domain.base_event import BaseEvent

E = TypeVar("E", bound=BaseEvent)


class IEventBus(ABC):
    """
    @brief Interface for the Event Bus (Pub/Sub mechanism).

    @details Allows different parts of the system to communicate loosely coupled.
    Supports both string-based event names and typed event classes inheriting from BaseEvent.

    @par Tutorial / Usage Example:
    @code
    # String-based:
    event_bus.on("user.created", on_user_created)
    event_bus.emit("user.created", new_user_obj)

    # Class-based (Typed):
    event_bus.on(UserCreatedEvent, lambda evt: print(evt.user_id))
    event_bus.emit(UserCreatedEvent(user_id=123))
    @endcode
    """

    @abstractmethod
    def emit(self, event_name_or_obj: str | BaseEvent | Any, data: Any = None) -> None:
        """
        @brief Publishes an event along with optional data.

        @param event_name_or_obj The event name or a BaseEvent object.
        @param data The data payload to pass to handlers if using event_name.
        """
        ...

    @abstractmethod
    def on(self, event_name_or_type: str | type[E] | Any, handler: Callable[..., Any]) -> None:
        """
        @brief Subscribes a handler function to an event.

        @param event_name_or_type The event name or BaseEvent subclass type.
        @param handler The function to call when the event occurs.
        """
        ...

    @abstractmethod
    def off(self, event_name_or_type: str | type[E] | Any, handler: Callable[..., Any]) -> None:
        """
        @brief Unsubscribes a handler function from an event.

        @param event_name_or_type The event name or BaseEvent subclass type.
        @param handler The function to remove.
        """
        ...
