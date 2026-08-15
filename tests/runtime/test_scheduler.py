import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from sagittarius_engine.runtime.scheduler.events import (
    SchedulerStarted,
    SchedulerStopped,
)
from sagittarius_engine.runtime.scheduler.scheduler import Scheduler
from sagittarius_engine.runtime.scheduler.triggers import CronTrigger


def test_scheduler_start_stop():
    context = MagicMock()
    scheduler = Scheduler(context)

    scheduler.start()
    assert scheduler._running is True
    assert scheduler._thread is not None
    assert scheduler._thread.is_alive()

    scheduler.stop()
    assert scheduler._running is False
    assert scheduler._thread is None


def test_scheduler_already_started():
    context = MagicMock()
    scheduler = Scheduler(context)

    scheduler.start()
    thread = scheduler._thread
    scheduler.start()
    assert scheduler._thread is thread  # Should not create a new thread

    scheduler.stop()


def test_scheduler_stop_not_running():
    context = MagicMock()
    scheduler = Scheduler(context)

    scheduler.stop()  # Should return immediately
    assert scheduler._thread is None


def test_scheduler_events():
    context = MagicMock()
    scheduler = Scheduler(context)

    scheduler.start()

    calls = context.event_bus.emit.call_args_list
    assert len(calls) == 1
    assert calls[0][0][0] == "runtime.scheduler.started"
    assert isinstance(calls[0][0][1], SchedulerStarted)

    context.event_bus.emit.reset_mock()
    scheduler.stop()

    calls = context.event_bus.emit.call_args_list
    assert len(calls) == 1
    assert calls[0][0][0] == "runtime.scheduler.stopped"
    assert isinstance(calls[0][0][1], SchedulerStopped)


def test_scheduler_emit_exception():
    context = MagicMock()
    context.event_bus.emit.side_effect = Exception("Emit failed")
    scheduler = Scheduler(context)

    # Should swallow exception
    scheduler.start()
    scheduler.stop()


def test_scheduler_add_after_job():
    context = MagicMock()
    scheduler = Scheduler(context)

    fn = MagicMock()
    fn.__name__ = "dummy_fn"

    scheduler.start()
    scheduler.after(seconds=0.1).do(fn)

    time.sleep(0.3)
    scheduler.stop()

    assert context.tasks.spawn.call_count == 1
    # Check the first argument of the first call
    spawn_call = context.tasks.spawn.call_args_list[0]
    assert spawn_call[0][0] == fn
    assert "ScheduledJob" in spawn_call[1]["name"]


def test_scheduler_add_every_job():
    context = MagicMock()
    scheduler = Scheduler(context)

    fn = MagicMock()
    fn.__name__ = "dummy_fn"

    scheduler.start()
    scheduler.every(seconds=0.1).do(fn)

    time.sleep(0.35)
    scheduler.stop()

    # Should run ~3 times (0.1, 0.2, 0.3)
    assert context.tasks.spawn.call_count >= 2


def test_scheduler_cron_trigger_builder():
    context = MagicMock()
    scheduler = Scheduler(context)

    job = scheduler.cron("*/5 * * * *").do(lambda: None)

    assert isinstance(job.trigger, CronTrigger)
    assert job.trigger.cron_expr == "*/5 * * * *"
    assert job in scheduler.jobs
    assert job.max_runs is None


def test_scheduler_job_execution_exception():
    context = MagicMock()
    context.tasks.spawn.side_effect = Exception("Spawn error")
    scheduler = Scheduler(context)

    def dummy():
        pass

    scheduler.start()
    scheduler.after(seconds=0.1).do(dummy)

    time.sleep(0.2)
    scheduler.stop()

    # It should not crash the scheduler thread, and it should call spawn
    assert context.tasks.spawn.call_count == 1


def test_scheduler_sleep_time_fallback():
    context = MagicMock()
    scheduler = Scheduler(context)

    with patch("sagittarius_engine.runtime.scheduler.scheduler.datetime") as mock_dt:
        t0 = datetime(2025, 1, 1, 12, 0, 0)
        mock_dt.now.side_effect = [t0, t0 + timedelta(seconds=2)]

        scheduler._running = True

        original_wait = scheduler._cond.wait

        def wait_side_effect(sleep_time):
            scheduler._running = False
            original_wait(sleep_time)

        with patch.object(
            scheduler._cond, "wait", side_effect=wait_side_effect
        ) as mock_wait:
            scheduler._run()

            mock_wait.assert_called_once_with(0.01)
