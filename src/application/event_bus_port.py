from abc import ABC, abstractmethod
from typing import Any, Callable

class IEventBus(ABC):
    @abstractmethod
    def emit(self, event_name: str, data: Any = None) -> None:
        ...

    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        ...

    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        ...
