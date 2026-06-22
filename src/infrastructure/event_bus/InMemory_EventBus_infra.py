import asyncio
from typing import Type, TypeVar, Callable, Awaitable, Dict, Any, List, Optional

from domain.event_bus.EventBus_api import Event, EventBus, EventHandler
from src.domain.logger import Logger

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

    async def publish(self, event: Event) -> None:
        tasks: List[Awaitable[None]] = []
        for event_type, handlers in list(self._handlers.items()):
            if isinstance(event, event_type):
                for handler in handlers:
                    if asyncio.iscoroutinefunction(handler):
                        tasks.append(self._run_async_handler(handler, event))
                    else:
                        self._run_sync_handler(handler, event)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _run_async_handler(
        self, handler: Callable[[Any], Awaitable[None]], event: Event
    ) -> None:
        try:
            await handler(event)
        except Exception as e:
            if self._logger:
                self._logger.exception(
                    f"Error executing async handler {getattr(handler, '__name__', str(handler))} for event {event.__class__.__name__}: {e}"
                )

    def _run_sync_handler(self, handler: Callable[[Any], None], event: Event) -> None:
        try:
            handler(event)
        except Exception as e:
            if self._logger:
                self._logger.exception(
                    f"Error executing sync handler {getattr(handler, '__name__', str(handler))} for event {event.__class__.__name__}: {e}"
                )
