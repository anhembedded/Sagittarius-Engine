import asyncio
import logging
from typing import Type, TypeVar, Callable, Awaitable, Union, Dict, Any, List

from src.domain.event_bus import Event, EventBus, EventHandler

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Event)


class InMemoryEventBus(EventBus):
    """
    In-memory concrete implementation of the EventBus interface.
    Supports asynchronous and synchronous handlers, executing them concurrently
    when an event is published.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}

    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(
                "Subscribed %s to %s",
                handler.__name__ if hasattr(handler, "__name__") else str(handler),
                event_type.__name__,
            )

    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]
            logger.debug(
                "Unsubscribed %s from %s",
                handler.__name__ if hasattr(handler, "__name__") else str(handler),
                event_type.__name__,
            )

    async def publish(self, event: Event) -> None:
        """
        Publishes the event to all registered handlers for the event type or any of its superclasses.
        Concurrently executes async handlers and runs sync handlers.
        Handles errors gracefully to prevent one failed handler from affecting others.
        """
        tasks: List[Awaitable[None]] = []

        # Identify matching handlers by checking if event is an instance of the registered type.
        # This allows handlers subscribed to a base class to receive events of subclasses.
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
            logger.exception(
                "Error executing async handler %s for event %s: %s",
                handler.__name__ if hasattr(handler, "__name__") else str(handler),
                event.__class__.__name__,
                e,
            )

    def _run_sync_handler(self, handler: Callable[[Any], None], event: Event) -> None:
        try:
            handler(event)
        except Exception as e:
            logger.exception(
                "Error executing sync handler %s for event %s: %s",
                handler.__name__ if hasattr(handler, "__name__") else str(handler),
                event.__class__.__name__,
                e,
            )
