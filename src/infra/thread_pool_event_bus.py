import concurrent.futures
from collections.abc import Callable
from typing import Any

from src.infra.memory_event_bus import MemoryEventBus
from src.interfaces import IEventBus, ILogger


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

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Emits an event, executing its handlers concurrently in a thread pool.

        @param event_name The name of the event.
        @param data The data payload.
        """
        if self.logger:
            self.logger.info(
                f"Emitting event: {event_name} to ThreadPoolEventBus with data: {data}"
            )

        # Snapshot handlers using inner bus lock
        with self._inner_bus._lock:
            handlers_snapshot = list(self._inner_bus._handlers.get(event_name, []))

        futures = []
        for handler in handlers_snapshot:
            futures.append(self._executor.submit(handler, data))

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

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Registers a handler.

        @param event_name The name of the event.
        @param handler The callback function.
        """
        self._inner_bus.on(event_name, handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unregisters a handler.

        @param event_name The name of the event.
        @param handler The callback function to remove.
        """
        self._inner_bus.off(event_name, handler)

    def shutdown(self, wait: bool = True) -> None:
        """
        @brief Shuts down the thread pool executor.

        @param wait Whether to wait for pending futures to complete.
        """
        self._executor.shutdown(wait=wait)
