import threading
from collections.abc import Callable
from typing import Any

from src.interfaces import IEventBus, ILogger


class MemoryEventBus(IEventBus):
    """
    @brief Synchronous In-memory implementation of IEventBus.

    @details Suitable for single-process applications or in test environments.
    When an event is emitted, all registered handlers are invoked immediately
    in the same thread.

    @par Tutorial / Usage Example:
    @code
    bus = MemoryEventBus(logger)

    # Handler function
    def send_email(data):
        print(f"Sending email to {data['email']}")

    # Subscription
    bus.on('user.registered', send_email)

    # Emit event
    bus.emit('user.registered', {'email': 'test@example.com'})
    @endcode
    """

    def __init__(self, logger: ILogger | None = None) -> None:
        """
        @brief Constructor.
        @param logger Optional logger instance.
        """
        self._handlers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Synchronously emits an event to all listening handlers.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting event: {event_name} with data: {data}")

        with self._lock:
            handlers_snapshot = list(self._handlers.get(event_name, []))

        for handler in handlers_snapshot:
            try:
                handler(data)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in handler {handler}: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
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
