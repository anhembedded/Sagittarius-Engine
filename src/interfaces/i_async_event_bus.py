from typing import Any, Callable, Protocol

class IAsyncEventBus(Protocol):
    """
    @brief Asynchronous EventBus interface for decoupled communication.
    """

    async def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Asynchronously emits an event to all registered handlers.
        """
        ...

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler for a specific event.
        """
        ...

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler for a specific event.
        """
        ...
