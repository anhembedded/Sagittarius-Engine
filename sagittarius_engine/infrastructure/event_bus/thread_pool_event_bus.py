import concurrent.futures
from collections.abc import Callable
from typing import Any

from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.interfaces import IEventBus, ILogger


class ThreadPoolEventBus(IEventBus):
    """
    @brief EventBus implementation that executes handlers in a ThreadPoolExecutor.

    @details Internally uses a thread-safe MemoryEventBus to manage handlers.
    When an event is emitted, handlers are submitted to a thread pool for execution.
    """

    def __init__(self, max_workers: int = 4, logger: ILogger | None = None) -> None:
        """
        @brief Constructor.
        @param max_workers Maximum number of threads in the pool.
        @param logger Optional logger instance.
        """
        self._inner_bus = MemoryEventBus(
            logger=None
        )  # We will manage logging locally for the pool
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logger

    def emit(self, event_name_or_obj: str | Any, data: Any = None) -> None:
        """
        @brief Emits an event, executing its handlers concurrently in a thread pool.

        @param event_name_or_obj The name of the event or BaseEvent object.
        @param data The data payload.
        """
        if isinstance(event_name_or_obj, str):
            event_name = event_name_or_obj
            payload = data
        else:
            event_name = (
                getattr(
                    event_name_or_obj,
                    "event_name",
                    type(event_name_or_obj).__qualname__,
                )
                or type(event_name_or_obj).__qualname__
            )
            payload = data if data is not None else event_name_or_obj
        if self.logger:
            self.logger.info(
                f"Emitting event: {event_name} to ThreadPoolEventBus with data: {payload}"
            )

        # Public handler access without inspecting private state
        if hasattr(self._inner_bus, "get_handlers"):
            handlers_snapshot = self._inner_bus.get_handlers(event_name_or_obj if not isinstance(event_name_or_obj, str) else event_name)
        else:
            handlers_snapshot = getattr(self._inner_bus, "_handlers", {}).get(event_name, ())

        futures = []
        for handler in handlers_snapshot:
            futures.append(self._executor.submit(handler, payload))

        for future in futures:

            def _log_error(f, event=event_name):
                try:
                    f.result()
                except Exception as exc:
                    if self.logger:
                        self.logger.error(
                            f"Error executing handler for event {event}: {exc}"
                        )

            future.add_done_callback(_log_error)

    def on(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        """
        @brief Registers a handler.

        @param event_name_or_type The name of the event or event type.
        @param handler The callback function.
        """
        self._inner_bus.on(event_name_or_type, handler)

    def off(self, event_name_or_type: str | Any, handler: Callable[..., Any]) -> None:
        """
        @brief Unregisters a handler.

        @param event_name_or_type The name of the event or event type.
        @param handler The callback function to remove.
        """
        self._inner_bus.off(event_name_or_type, handler)

    def shutdown(self, wait: bool = True) -> None:
        """
        @brief Shuts down the thread pool executor.

        @param wait Whether to wait for pending futures to complete.
        """
        self._executor.shutdown(wait=wait)

    def get_handlers(
        self, event_name_or_type: str | Any
    ) -> tuple[Callable[..., Any], ...]:
        """
        @brief Returns registered handlers for an event.
        """
        if hasattr(self._inner_bus, "get_handlers"):
            return self._inner_bus.get_handlers(event_name_or_type)
        return ()
