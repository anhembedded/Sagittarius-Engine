import pytest

from sagittarius_engine.runtime.tasks.background_task import BackgroundTask, TaskState


def test_background_task_initialization():
    task = BackgroundTask(name="TestTask")
    assert task.name == "TestTask"
    assert task.status == TaskState.PENDING
    assert task.progress == 0.0
    assert task.id is not None
    assert task.start_time is not None
    assert task.end_time is None


def test_background_task_state_transitions():
    task = BackgroundTask(name="StateTask")

    task.status = TaskState.RUNNING
    assert task.status == TaskState.RUNNING
    assert task.end_time is None

    task.status = TaskState.COMPLETED
    assert task.status == TaskState.COMPLETED
    assert task.end_time is not None


def test_background_task_progress_update():
    events_emitted = []

    def mock_on_progress(val, msg):
        events_emitted.append((val, msg))

    task = BackgroundTask(name="ProgressTask", on_progress_update=mock_on_progress)

    task.update_progress(50.0, "Halfway there")
    assert task.progress == 50.0
    assert len(events_emitted) == 1
    assert events_emitted[0] == (50.0, "Halfway there")


def test_background_task_invalid_progress():
    task = BackgroundTask(name="InvalidProgressTask")

    with pytest.raises(ValueError, match="Progress must be between 0.0 and 100.0"):
        task.update_progress(-10.0)

    with pytest.raises(ValueError, match="Progress must be between 0.0 and 100.0"):
        task.update_progress(101.0)
