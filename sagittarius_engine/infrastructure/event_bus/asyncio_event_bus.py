import asyncio
import inspect
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IAsyncEventBus, ILogger


class AsyncioEventBus(IAsyncEventBus):
    """
    @brief Asynchronous EventBus implementation using asyncio.

    @details Allows handlers to be standard sync functions or async coroutines.
    Handlers are awaited sequentially within the asyncio event loop.
    """

    def __init__(self, logger: ILogger | None = None) -> None:
        """
        @brief Constructor.
        @param logger Optional logger instance.
        """
        self._handlers: dict[str, tuple[Callable, ...]] = {}
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

        # Lock-free read using Copy-On-Write tuple
        handlers_snapshot = self._handlers.get(event_name, ())

        for handler in handlers_snapshot:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except asyncio.CancelledError as e:
                if self.logger:
                    self.logger.error(
                        f"Async handler cancelled for event {event_name}: {e}"
                    )
            except Exception as e:
                if self.logger:
                    self.logger.error(
                        f"Error executing async handler for event {event_name}: {e}"
                    )

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function (can be sync or async).
        """
        with self._lock:
            handlers = self._handlers.get(event_name, ())
            if handler not in handlers:
                self._handlers[event_name] = handlers + (handler,)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        with self._lock:
            handlers = self._handlers.get(event_name, ())
            if handler in handlers:
                self._handlers[event_name] = tuple(h for h in handlers if h != handler)
                if not self._handlers[event_name]:
                    del self._handlers[event_name]
