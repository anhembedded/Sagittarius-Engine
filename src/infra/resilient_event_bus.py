from typing import Any, Callable, List, Tuple, Optional
from src.core import IEventBus, ILogger

class ResilientEventBus(IEventBus):
    def __init__(self, inner_bus: IEventBus, max_retries: int = 3, logger: Optional[ILogger] = None) -> None:
        self.inner_bus = inner_bus
        self.max_retries = max_retries
        self._dlq: List[Tuple[str, Any, Callable, Exception]] = []
        self.logger = logger

        # We need to hook into the inner bus emit logic, but since IEventBus
        # doesn't expose handlers directly, we intercept registration.
        self._handlers: dict[str, list[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
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

            # Note: We do not call inner_bus.emit because we manage handlers here
            # to be able to wrap their execution. This is a decorator over IEventBus.
            # Alternatively, if we just use inner_bus to store handlers, we wouldn't
            # be able to wrap the loop. So ResilientEventBus acts as a full EventBus
            # but could sync handlers to inner_bus if strictly required.

    def on(self, event_name: str, handler: Callable) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
        self.inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
        self.inner_bus.off(event_name, handler)

    def get_dlq(self) -> List[Tuple[str, Any, Callable, Exception]]:
        return list(self._dlq)

    def reprocess(self) -> None:
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
