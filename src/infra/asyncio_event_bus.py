import asyncio
import threading
from typing import Any, Callable, Optional
from src.interfaces import IAsyncEventBus, ILogger

class AsyncioEventBus(IAsyncEventBus):
    """
    @brief Asynchronous EventBus implementation using asyncio.

    @details Allows handlers to be standard sync functions or async coroutines.
    Handlers are awaited sequentially within the asyncio event loop.
    """
    def __init__(self, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.
        @param logger Optional logger instance.
        """
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    async def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Asynchronously emits an event to all listening handlers sequentially.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting async event: {event_name} with data: {data}")

        with self._lock:
            handlers_snapshot = list(self._handlers.get(event_name, []))

        for handler in handlers_snapshot:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error executing async handler for event {event_name}: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function (can be sync or async).
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        with self._lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
