from typing import Any, Callable, List, Tuple, Optional
from src.core import IEventBus, ILogger

class ResilientEventBus(IEventBus):
    """
    @brief A Decorator for IEventBus that adds Retry mechanisms and a Dead Letter Queue (DLQ).

    @details If a handler throws an exception while processing an event, the ResilientEventBus
    will attempt to call the handler again (Retry). If the max retries are exceeded,
    the event is pushed into the DLQ for manual processing later (Reprocess).

    @par Tutorial / Usage Example:
    @code
    # Wrap a basic event bus
    base_bus = MemoryEventBus()
    safe_bus = ResilientEventBus(inner_bus=base_bus, max_retries=3)

    # If an emit consistently fails, it goes to the DLQ
    safe_bus.emit("some.event", data)

    # Inspect failed events
    failed_events = safe_bus.get_dlq()

    # Attempt to re-run the failed events
    safe_bus.reprocess()
    @endcode
    """
    def __init__(self, inner_bus: IEventBus, max_retries: int = 3, logger: Optional[ILogger] = None) -> None:
        """
        @brief Constructor.

        @param inner_bus The base event bus to decorate.
        @param max_retries The maximum number of retries before adding to DLQ.
        @param logger Optional logger instance.
        """
        self.inner_bus = inner_bus
        self.max_retries = max_retries
        self._dlq: List[Tuple[str, Any, Callable, Exception]] = []
        self.logger = logger

        self._handlers: dict[str, list[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Emits an event with a built-in retry mechanism.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(f"Emitting resilient event: {event_name} with data: {data}")

        for handler in self._handlers.get(event_name, []):
            success = False
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    success = True
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
        self.inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
        self.inner_bus.off(event_name, handler)

    def get_dlq(self) -> List[Tuple[str, Any, Callable, Exception]]:
        """
        @brief Retrieves the Dead Letter Queue.
        @return A list of failed events stored in the DLQ.
        """
        return list(self._dlq)

    def reprocess(self) -> None:
        """
        @brief Attempts to reprocess all events currently in the DLQ.
        """
        current_dlq = self._dlq
        self._dlq = []
        for event_name, data, handler, _ in current_dlq:
            success = False
            for attempt in range(self.max_retries + 1):
                try:
                    handler(data)
                    success = True
                    break
                except Exception as e:
                    if attempt == self.max_retries:
                        self._dlq.append((event_name, data, handler, e))
