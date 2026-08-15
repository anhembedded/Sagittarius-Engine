import time
from unittest.mock import Mock
from sagittarius_engine.runtime.tasks.task_manager import TaskManager
from sagittarius_engine.runtime.tasks.background_task import TaskState
from sagittarius_engine.runtime.tasks.events import TaskProgressUpdated


class MockContext:
    def __init__(self):
        self.event_bus = Mock()
        self.async_runtime = Mock()


def test_task_manager_spawn_sync_task():
    context = MockContext()
    manager = TaskManager(context)

    def dummy_task(token=None):
        time.sleep(0.1)
        return "done"

    task = manager.spawn(dummy_task, name="SyncTest")
    assert task.status == TaskState.RUNNING
    assert task.name == "SyncTest"

    # Wait for completion
    task.future.result(timeout=2.0)

    # Needs a slight delay for the wrapper to update state
    time.sleep(0.1)
    assert task.status == TaskState.COMPLETED


def test_task_manager_progress_event_emission():
    context = MockContext()
    manager = TaskManager(context)

    def progress_task(token=None):
        pass  # We will just manually trigger update_progress

    task = manager.spawn(progress_task, name="ProgressTask")

    # Manually trigger progress
    task.update_progress(75.5, "Almost there")

    # Verify event_bus.emit was called with TaskProgressUpdated
    emit_calls = context.event_bus.emit.call_args_list
    progress_calls = [
        call for call in emit_calls if call.args[0] == "runtime.tasks.progress"
    ]

    assert len(progress_calls) >= 1
    event_obj = progress_calls[0].args[1]
    assert isinstance(event_obj, TaskProgressUpdated)
    assert event_obj.task_id == task.id
    assert event_obj.progress == 75.5
    assert event_obj.message == "Almost there"


def test_task_manager_cleanup():
    from sagittarius_engine.runtime.tasks.background_task import (
        BackgroundTask,
        TaskState,
    )

    context = MockContext()
    manager = TaskManager(context)

    # Add 200 completed tasks
    for i in range(200):
        t = BackgroundTask(f"completed_task_{i}")
        t.status = TaskState.COMPLETED
        manager.tasks[t.id] = t
        manager._finished_task_ids.append(t.id)

    # Add 5 active tasks
    for i in range(5):
        t = BackgroundTask(f"active_task_{i}")
        t.status = TaskState.RUNNING
        manager.tasks[t.id] = t

    manager._cleanup_old_tasks()

    assert len(manager._finished_task_ids) == 50
    assert len(manager.tasks) == 55
