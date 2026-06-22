from typing import Type, TypeVar, Callable, Dict, Any, List, Optional

from src.domain.event_bus.EventBus_api import Event, EventBus, EventHandler
from src.domain.logger.Logger_api import Logger

T = TypeVar("T", bound=Event)

class InMemoryEventBusInfra(EventBus):
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}
        self._logger = logger

    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            if self._logger:
                self._logger.debug(
                    f"Subscribed {getattr(handler, '__name__', str(handler))} to {event_type.__name__}"
                )

    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]
            if self._logger:
                self._logger.debug(
                    f"Unsubscribed {getattr(handler, '__name__', str(handler))} from {event_type.__name__}"
                )

    def publish(self, event: Event) -> None:
        for event_type, handlers in list(self._handlers.items()):
            if isinstance(event, event_type):
                for handler in handlers:
                    self._run_handler(handler, event)

    def _run_handler(self, handler: Callable[[Any], None], event: Event) -> None:
        try:
            handler(event)
        except Exception as e:
            if self._logger:
                self._logger.exception(
                    f"Error executing handler {getattr(handler, '__name__', str(handler))} for event {event.__class__.__name__}: {e}"
                )
