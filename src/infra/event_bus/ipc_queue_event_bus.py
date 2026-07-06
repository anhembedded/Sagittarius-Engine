import queue
import threading
import logging
from collections.abc import Callable
from multiprocessing.queues import Queue
from typing import Any

from src.interfaces.i_event_bus import IEventBus
from src.interfaces.i_logger import ILogger


class IPCBroker:
    """
    @brief Broker for events to multiple subscriber queues.
    """

    def __init__(self, publish_queue: Queue, logger: ILogger | None = None):
        self._publish_queue = publish_queue
        self._subscriber_queues: list[Queue] = []
        self._logger = logger
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def add_subscriber(self, sub_queue: Queue) -> None:
        """Adds a subscriber queue to receive broadcasted events."""
        with self._lock:
            if sub_queue not in self._subscriber_queues:
                self._subscriber_queues.append(sub_queue)

    def remove_subscriber(self, sub_queue: Queue) -> None:
        """Removes a subscriber queue."""
        with self._lock:
            if sub_queue in self._subscriber_queues:
                self._subscriber_queues.remove(sub_queue)

    def start(self) -> None:
        """Starts the broker loop in a background daemon thread."""
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="IPCBrokerThread"
        )
        self._thread.start()
        if self._logger:
            self._logger.info("IPCBroker started.")

    def stop(self) -> None:
        """Stops the broker loop gracefully."""
        self._stop_event.set()
        # To unblock the get(), put a sentinel value in the publish queue
        try:
            self._publish_queue.put(("_STOP_", None))
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error stopping IPCBroker: {e}")

        if self._thread:
            self._thread.join(timeout=2.0)

        if self._logger:
            self._logger.info("IPCBroker stopped.")

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                # We use a timeout so it can check stop_event periodically
                # if the sentinel fails or isn't used
                message = self._publish_queue.get(timeout=0.1)

                # Check for sentinel
                if (
                    isinstance(message, tuple)
                    and len(message) == 2
                    and message[0] == "_STOP_"
                ):
                    break

                event_name, data = message

                with self._lock:
                    for sub_queue in self._subscriber_queues:
                        try:
                            sub_queue.put((event_name, data))
                        except Exception as e:
                            if self._logger:
                                self._logger.error(
                                    f"Failed to route event {event_name} "
                                    f"to a subscriber: {e}"
                                )
                            else:
                                logging.error(
                                    f"Failed to route event {event_name} "
                                    f"to a subscriber: {e}"
                                )

            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f"IPCBroker encountered an error: {e}")
                else:
                    logging.error(f"IPCBroker encountered an error: {e}")


class IPCQueueEventBus(IEventBus):
    """
    @brief IPC Event Bus that uses Queue for cross-process Pub/Sub.
    """

    def __init__(
        self,
        subscriber_queue: Queue | None = None,
        publish_queue: Queue | None = None,
        logger: ILogger | None = None,
    ):
        self._subscriber_queue = subscriber_queue
        self._publish_queue = publish_queue
        self._logger = logger

        self._handlers: dict[str, list[Callable]] = {}
        self._handlers_lock = threading.Lock()

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        @brief Publishes an event to the shared publish queue.
        """
        if not self._publish_queue:
            if self._logger:
                self._logger.warning(
                    f"Cannot emit '{event_name}': publish_queue is None."
                )
            else:
                logging.warning(f"Cannot emit '{event_name}': publish_queue is None.")
            return

        try:
            self._publish_queue.put((event_name, data))
        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"Failed to emit event '{event_name}' to publish_queue: {e}"
                )
            else:
                logging.error(f"Failed to emit event '{event_name}' to publish_queue: {e}")

    def on(self, event_name: str, handler: Callable) -> None:
        """
        @brief Subscribes a local handler to an event.
        """
        with self._handlers_lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable) -> None:
        """
        @brief Unsubscribes a local handler from an event.
        """
        with self._handlers_lock:
            if event_name in self._handlers and handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
                if not self._handlers[event_name]:
                    del self._handlers[event_name]

    def start(self) -> None:
        """
        @brief Starts the daemon thread to listen on the subscriber queue.
        """
        if not self._subscriber_queue:
            if self._logger:
                self._logger.warning(
                    "No subscriber_queue provided; IPCQueueEventBus "
                    "will not listen for events."
                )
            return

        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="IPCQueueEventBusListener"
        )
        self._thread.start()

        if self._logger:
            self._logger.info("IPCQueueEventBus listener started.")

    def stop(self) -> None:
        """
        @brief Stops the listener daemon thread gracefully.
        """
        self._stop_event.set()

        if self._subscriber_queue:
            # Put sentinel to unblock
            try:
                self._subscriber_queue.put(("_STOP_", None))
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Error stopping IPCQueueEventBus: {e}")

        if self._thread:
            self._thread.join(timeout=2.0)

        if self._logger:
            self._logger.info("IPCQueueEventBus listener stopped.")

    def _run(self) -> None:
        if not self._subscriber_queue:
            return

        while not self._stop_event.is_set():
            try:
                message = self._subscriber_queue.get(timeout=0.1)  # type: ignore

                # Check for sentinel
                if (
                    isinstance(message, tuple)
                    and len(message) == 2
                    and message[0] == "_STOP_"
                ):
                    break

                event_name, data = message
                self._dispatch(event_name, data)

            except queue.Empty:
                continue
            except Exception as e:
                if self._logger:
                    self._logger.error(f"IPCQueueEventBus listener error: {e}")

    def _dispatch(self, event_name: str, data: Any) -> None:
        """Calls all local handlers registered for the event."""
        with self._handlers_lock:
            # Copy list to allow modifications during handler execution
            handlers = self._handlers.get(event_name, []).copy()

        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Error in IPC handler for '{event_name}': {e}")
