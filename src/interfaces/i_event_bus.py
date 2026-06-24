from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional

class IEventBus(ABC):
    """
    @brief Interface for the Event Bus (Pub/Sub mechanism).

    @details Allows different parts of the system to communicate loosely coupled.

    @par Tutorial / Usage Example:
    @code
    def on_user_created(user):
        print(f"Sending welcome email to {user.email}")

    event_bus.on("user.created", on_user_created)
    event_bus.emit("user.created", new_user_obj)
    @endcode
    """

    @abstractmethod
    def emit(self, event_name: str, data: Any=None) -> None:
        """
        @brief Publishes an event along with optional data.

        @param event_name The name of the event to emit.
        @param data The data payload to pass to handlers.
        """
        ...

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Subscribes a handler function to an event.

        @param event_name The name of the event.
        @param handler The function to call when the event occurs.
        """
        ...

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unsubscribes a handler function from an event.

        @param event_name The name of the event.
        @param handler The function to remove.
        """
        ...
