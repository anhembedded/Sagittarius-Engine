import concurrent.futures
import threading
from collections.abc import Callable
from typing import Any

from sagittarius_engine.interfaces.i_thread_manager import (
    IThreadManager,
)


class ThreadManager(IThreadManager):
    """!
    @brief ThreadManager implementation using ThreadPoolExecutor.

    This class provides a centralized thread pool for executing background tasks.
    It implements the IThreadManager interface.
    """

    def __init__(self, max_workers: int = 4) -> None:
        """!
        @brief Initialize the ThreadManager.

        @param max_workers The maximum number of threads to use in the pool.
        """
        self._max_workers = max_workers
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_workers
        )
        self._lock = threading.Lock()

    def submit(
        self, task: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> concurrent.futures.Future[Any]:
        """!
        @brief Submit a task to be executed by the thread pool.

        @param task The callable task to execute.
        @param args Positional arguments for the task.
        @param kwargs Keyword arguments for the task.
        @return A Future representing the execution of the task.
        """
        with self._lock:
            return self._executor.submit(task, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        """!
        @brief Shut down the thread pool.

        @param wait If True, blocks until all pending tasks are completed.
        """
        with self._lock:
            self._executor.shutdown(wait=wait)
