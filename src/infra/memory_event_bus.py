from typing import Any, Callable
from src.core import IEventBus

class MemoryEventBus(IEventBus):
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = {}

    def emit(self, event_name: str, data: Any = None) -> None:
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
