from typing import Any, Callable, Optional
from src.core import IEventBus, ILogger

class MemoryEventBus(IEventBus):
    def __init__(self, logger: Optional[ILogger] = None) -> None:
        self._handlers: dict[str, list[Callable]] = {}
        self.logger = logger

    def emit(self, event_name: str, data: Any = None) -> None:
        if self.logger:
            self.logger.info(f"Emitting event: {event_name} with data: {data}")

        for handler in self._handlers.get(event_name, []):
            handler(data)

    def on(self, event_name: str, handler: Callable) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)
