import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces import IEventBus, ILogger


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
        self._handlers: dict[str, tuple[Callable, ...]] = {}
        self._lock = threading.Lock()
        self.logger = logger

    def _get_event_key(self, event_name_or_type: str | type | Any) -> str:
        if isinstance(event_name_or_type, str):
            return event_name_or_type
        key = getattr(event_name_or_type, "event_name", None)
        if key:
            return key
        if isinstance(event_name_or_type, type):
            return event_name_or_type.__qualname__
        return event_name_or_type.__class__.__qualname__

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        """
        @brief Synchronously emits an event to all listening handlers.

        @param event_name_or_obj Event string name or BaseEvent object instance.
        @param data The data payload (if event_name string is used).
        """
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = self._get_event_key(event_name_or_obj)
            payload = data if data is not None else event_name_or_obj

        if self.logger:
            self.logger.info(f"Emitting event: {event_name} with data: {payload}")

        # ⚡ Bolt: Lock-free read using Copy-On-Write pattern to reduce contention
        handlers_snapshot = self._handlers.get(event_name, ())

        for handler in handlers_snapshot:
            try:
                handler(payload)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in handler {handler}: {e}")

    def on(self, event_name_or_type: str | type | Any, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name_or_type The name or class type of the event.
        @param handler The callback function.
        """
        key = self._get_event_key(event_name_or_type)
        with self._lock:
            current_handlers = self._handlers.get(key, ())
            if handler not in current_handlers:
                self._handlers[key] = current_handlers + (handler,)

    def off(self, event_name_or_type: str | type | Any, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name_or_type The name or class type of the event.
        @param handler The callback function to remove.
        """
        key = self._get_event_key(event_name_or_type)
        with self._lock:
            if key in self._handlers and handler in self._handlers[key]:
                self._handlers[key] = tuple(
                    h for h in self._handlers[key] if h != handler
                )
