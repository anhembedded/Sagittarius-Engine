import asyncio
from typing import Type, TypeVar, Callable, Awaitable, Dict, Any, List, Optional

from src.domain.event_bus import Event, EventBus, EventHandler
from src.domain.logger import Logger

T = TypeVar("T", bound=Event)


class InMemoryEventBus(EventBus):
    """
    In-memory implementation of the EventBus interface for local event distribution.
    Supports both synchronous and asynchronous handlers, executing them concurrently during publication.
    """

    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Initializes the in-memory event bus with an optional logger.
        Why: Sets up internal storage for handlers and provides observability through the injected logger.
        """
        self._handlers: Dict[Type[Event], List[EventHandler[Any]]] = {}
        self._logger = logger

    def subscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Registers a handler for a specific event type.
        Why: Enables the handler to receive and process events of the given type.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            if self._logger:
                self._logger.debug(
                    "Subscribed %s to %s",
                    handler.__name__ if hasattr(handler, "__name__") else str(handler),
                    event_type.__name__,
                )

    def unsubscribe(self, event_type: Type[T], handler: EventHandler[T]) -> None:
        """
        Removes a handler registration for an event type.
        Why: Stops the handler from receiving future events and manages resource lifecycle.
        """
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]
            if self._logger:
                self._logger.debug(
                    "Unsubscribed %s from %s",
                    handler.__name__ if hasattr(handler, "__name__") else str(handler),
                    event_type.__name__,
                )

    async def publish(self, event: Event) -> None:
        """
        Publishes an event to all registered handlers for its type or any of its superclasses.
        Why: Triggers concurrent execution of handlers to react to domain occurrences across the system.
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
        """
        Executes an asynchronous handler and catches any exceptions to ensure robustness.
        Why: Prevents a single failing handler from disrupting the overall publication process.
        """
        try:
            await handler(event)
        except Exception as e:
            if self._logger:
                self._logger.exception(
                    "Error executing async handler %s for event %s: %s",
                    handler.__name__ if hasattr(handler, "__name__") else str(handler),
                    event.__class__.__name__,
                    e,
                )

    def _run_sync_handler(self, handler: Callable[[Any], None], event: Event) -> None:
        """
        Executes a synchronous handler and catches any exceptions to ensure robustness.
        Why: Prevents a single failing handler from disrupting the overall publication process.
        """
        try:
            handler(event)
        except Exception as e:
            if self._logger:
                self._logger.exception(
                    "Error executing sync handler %s for event %s: %s",
                    handler.__name__ if hasattr(handler, "__name__") else str(handler),
                    event.__class__.__name__,
                    e,
                )
