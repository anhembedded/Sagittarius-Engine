import time
import pytest
from sagittarius_engine.kernel.app import App
from sagittarius_engine.runtime.hosted.hosted_service import IHostedService
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


class DummyHostedService(IHostedService):
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.started = False
        self.stopped = False

    def start(self, context) -> None:
        if self.should_fail:
            raise RuntimeError("Start failed")
        self.started = True

    def stop(self, context) -> None:
        self.stopped = True


def test_hosted_service_lifecycle_and_rollback():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    srv_a = DummyHostedService()
    srv_b = DummyHostedService()

    app.context.hosted_services.register(srv_a)
    app.context.hosted_services.register(srv_b)

    # Listen to events
    events = []
    event_bus.on(
        "runtime.hosted.started",
        lambda e: events.append(("started", e.service_name)),
    )
    event_bus.on(
        "runtime.hosted.stopped",
        lambda e: events.append(("stopped", e.service_name)),
    )

    # Start Hosted Services
    app.context.hosted_services.start()

    assert srv_a.started is True
    assert srv_b.started is True
    assert len(events) == 2
    assert events[0] == ("started", "DummyHostedService")

    # Stop Hosted Services
    app.context.hosted_services.stop()

    assert srv_a.stopped is True
    assert srv_b.stopped is True
    assert len(events) == 4
    assert events[2] == ("stopped", "DummyHostedService")

    # Test Rollback
    app2 = App(StdLibContainer(), MemoryEventBus())
    srv_ok = DummyHostedService()
    srv_err = DummyHostedService(should_fail=True)

    app2.context.hosted_services.register(srv_ok)
    app2.context.hosted_services.register(srv_err)

    with pytest.raises(RuntimeError, match="Start failed"):
        app2.context.hosted_services.start()

    assert srv_ok.started is True
    assert srv_ok.stopped is True  # Stopped during rollback!
    assert srv_err.started is False


def test_cancellation_token():
    token = CancellationToken()
    assert token.is_cancelled() is False

    token.cancel()
    assert token.is_cancelled() is True
    assert token.is_cancellation_requested is True

    # Test wait with short timeout
    token2 = CancellationToken()
    res = token2.wait(timeout=0.01)
    assert res is False  # Timed out

    def cancel_later():
        time.sleep(0.02)
        token2.cancel()

    import threading

    t = threading.Thread(target=cancel_later)
    t.start()
    res2 = token2.wait(timeout=1.0)
    assert res2 is True  # Cancelled!
    t.join()


def test_task_manager_sync_and_async():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.context.async_runtime.start()

    events = []
    event_bus.on(
        "runtime.tasks.started", lambda e: events.append(("started", e.task_name))
    )
    event_bus.on(
        "runtime.tasks.completed",
        lambda e: events.append(("completed", e.task_name)),
    )
    event_bus.on(
        "runtime.tasks.failed", lambda e: events.append(("failed", e.task_name))
    )

    # 1. Sync Task
    executed = False

    def sync_work():
        nonlocal executed
        executed = True
        return "sync_result"

    task = app.context.tasks.spawn(sync_work, name="SyncTask")
    task.future.result(timeout=1.0)

    assert executed is True
    assert task.status == "completed"

    # 2. Async Task
    async_executed = False

    async def async_work(token):
        nonlocal async_executed
        async_executed = True
        return "async_result"

    task2 = app.context.tasks.spawn(async_work, name="AsyncTask")
    res = task2.future.result(timeout=1.0)

    assert async_executed is True
    assert res == "async_result"
    assert task2.status == "completed"

    # 3. Failing Task
    def failing_work():
        raise ValueError("Oops")

    task3 = app.context.tasks.spawn(failing_work, name="FailingTask")
    with pytest.raises(Exception):
        task3.future.result(timeout=1.0)

    assert task3.status == "failed"

    # Wait for events to process
    time.sleep(0.05)
    event_names = [e[0] for e in events]
    assert "started" in event_names
    assert "completed" in event_names
    assert "failed" in event_names

    app.context.async_runtime.stop()
    app.context.tasks.shutdown()


def test_scheduler_fixed_interval():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Scheduler depends on tasks and async_runtime being started
    app.context.async_runtime.start()

    events = []
    event_bus.on("runtime.scheduler.started", lambda e: events.append("started"))
    event_bus.on("runtime.scheduler.stopped", lambda e: events.append("stopped"))

    app.context.scheduler.start()

    run_count = 0

    def job():
        nonlocal run_count
        run_count += 1

    # Schedule recurring job every 10ms
    app.context.scheduler.every(seconds=0.01).do(job)

    # Let it run a few times
    deadline = time.time() + 0.5
    while run_count < 2 and time.time() < deadline:
        time.sleep(0.01)

    assert run_count >= 2
    assert "started" in events

    # Check error robustness
    failing_runs = 0

    def bad_job():
        nonlocal failing_runs
        failing_runs += 1
        raise RuntimeError("Job failed")

    app.context.scheduler.every(seconds=0.01).do(bad_job)
    deadline = time.time() + 0.5
    while failing_runs < 1 and time.time() < deadline:
        time.sleep(0.01)

    assert failing_runs >= 1
    assert run_count >= 3  # Good job continues running!

    app.context.scheduler.stop()
    app.context.async_runtime.stop()
    app.context.tasks.shutdown()

    assert "stopped" in events


def test_graceful_shutdown():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()

    # Schedule a recurring job
    job_called = False

    def my_job():
        nonlocal job_called
        job_called = True

    app.context.scheduler.every(seconds=0.01).do(my_job)
    time.sleep(0.02)

    assert app.context.lifecycle.is_booted is True

    # Shutdown
    app.stop()

    assert app.context.lifecycle.is_stopped is True
    assert getattr(app.context.scheduler, "_thread", None) is None or not app.context.scheduler._thread.is_alive()
    assert getattr(app.context.async_runtime, "_thread", None) is None or not app.context.async_runtime._thread.is_alive()
