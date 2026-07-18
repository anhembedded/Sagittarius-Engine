import inspect
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional, Union

from sagittarius_engine.interfaces.events import (
    TaskCompleted,
    TaskFailed,
    TaskStarted,
)
from sagittarius_engine.runtime.tasks.background_task import BackgroundTask
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken


class TaskManager:
    """
    @brief Unified manager for spawning, tracking, and coordinating sync and async tasks.
    """

    def __init__(self, context: Any) -> None:
        self.context = context
        self.tasks: Dict[str, BackgroundTask] = {}
        self.executor = ThreadPoolExecutor(
            max_workers=20, thread_name_prefix="SagittariusTask"
        )
        self._lock = threading.Lock()
        self._logger = logging.getLogger("App")

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception:
            pass

    def _cleanup_old_tasks(self) -> None:
        with self._lock:
            # Prevent memory leaks by capping the tracking list of finished tasks
            if len(self.tasks) > 200:
                finished_ids = [
                    tid
                    for tid, t in self.tasks.items()
                    if t.status in ("completed", "failed", "cancelled")
                ]
                # Remove oldest finished tasks, keeping only the most recent 50
                for tid in finished_ids[:-50]:
                    del self.tasks[tid]

    def _wrap_sync(
        self, bg_task: BackgroundTask, fn: Callable[[], Any]
    ) -> Callable[[], Any]:
        def wrapper():
            try:
                res = fn()
                bg_task.status = "completed"
                self._emit(
                    "runtime.tasks.completed",
                    TaskCompleted(bg_task.id, bg_task.name),
                )
                return res
            except Exception as e:
                bg_task.status = "failed"
                bg_task.error = e
                self._logger.error(f"Task '{bg_task.name}' failed: {e}")
                self._emit(
                    "runtime.tasks.failed",
                    TaskFailed(bg_task.id, bg_task.name, e),
                )
                raise e
            finally:
                self._cleanup_old_tasks()

        return wrapper

    async def _wrap_coro(self, bg_task: BackgroundTask, coro: Any) -> Any:
        try:
            res = await coro
            bg_task.status = "completed"
            self._emit(
                "runtime.tasks.completed", TaskCompleted(bg_task.id, bg_task.name)
            )
            return res
        except Exception as e:
            bg_task.status = "failed"
            bg_task.error = e
            self._logger.error(f"Async task '{bg_task.name}' failed: {e}")
            self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, bg_task.name, e))
            raise e
        finally:
            self._cleanup_old_tasks()

    def spawn(
        self,
        callable_or_coro: Union[Callable[..., Any], Any],
        name: Optional[str] = None,
        token: Optional[CancellationToken] = None,
    ) -> BackgroundTask:
        """
        @brief Spawns a background execution (sync thread or async coroutine).
        """
        task_name = name or (
            callable_or_coro.__name__
            if hasattr(callable_or_coro, "__name__")
            else "UnnamedTask"
        )
        bg_task = BackgroundTask(task_name, token)

        with self._lock:
            self.tasks[bg_task.id] = bg_task

        self._emit("runtime.tasks.started", TaskStarted(bg_task.id, task_name))

        # Check if it's an async callable or a coroutine object
        if inspect.iscoroutinefunction(callable_or_coro) or inspect.iscoroutine(
            callable_or_coro
        ):
            # It's async
            coro = (
                callable_or_coro
                if inspect.iscoroutine(callable_or_coro)
                else callable_or_coro(bg_task.token)
            )
            bg_task.status = "running"
            try:
                future = self.context.async_runtime.run_coroutine(
                    self._wrap_coro(bg_task, coro)
                )
                bg_task.future = future
            except Exception as e:
                bg_task.status = "failed"
                bg_task.error = e
                self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e))
                raise e
        else:
            # It's sync
            bg_task.status = "running"
            try:
                sig = inspect.signature(callable_or_coro)
                if "token" in sig.parameters:
                    fn = lambda: callable_or_coro(token=bg_task.token)
                else:
                    fn = lambda: callable_or_coro()

                future = self.executor.submit(self._wrap_sync(bg_task, fn))
                bg_task.future = future
            except Exception as e:
                bg_task.status = "failed"
                bg_task.error = e
                self._emit("runtime.tasks.failed", TaskFailed(bg_task.id, task_name, e))
                raise e

        return bg_task

    def cancel_all(self) -> None:
        """
        @brief Cancels all currently running tasks.
        """
        with self._lock:
            for task in self.tasks.values():
                if task.status == "running":
                    task.cancel()

    def shutdown(self) -> None:
        """
        @brief Gracefully stops all tasks and shuts down the thread pool executor.
        """
        self.cancel_all()
        self.executor.shutdown(wait=True)
