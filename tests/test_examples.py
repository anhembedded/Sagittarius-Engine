import os
import sys
import time
import pytest
import subprocess
import threading


def run_example_script(script_path: str) -> None:
    # Set up PYTHONPATH so the examples can locate sagittarius_engine in the parent directory
    env = os.environ.copy()
    current_workspace = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    env["PYTHONPATH"] = (
        f"{current_workspace}{os.pathsep}{env.get('PYTHONPATH', '')}"
    )

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Error in {script_path}:\n{result.stderr}"


def test_examples_runnability():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "examples")
    )

    example_scripts = [
        "trading_bot/main.py",
        "desktop/main.py",
        "rest_api/main.py",
        "worker/main.py",
        "websocket/main.py",
        "plugin_system/main.py",
    ]

    for path in example_scripts:
        full_path = os.path.join(base_dir, path)
        assert os.path.exists(full_path)
        run_example_script(full_path)


def test_stress_boot_shutdown_cycles():
    # Stress test: boot and shutdown the engine repeatedly (10 cycles)
    # This verifies that resources, ports, event listeners, and threads are cleared cleanly
    from sagittarius_engine import App
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )

    initial_thread_count = threading.active_count()

    for _ in range(10):
        app = App(StdLibContainer(), MemoryEventBus())
        app.boot()
        app.stop()

    # Allow daemon threads some time to tear down if any
    time.sleep(0.05)
    final_thread_count = threading.active_count()

    # We shouldn't leak any non-daemon active threads
    assert (
        final_thread_count <= initial_thread_count + 1
    ), f"Thread leak detected! Initial: {initial_thread_count}, Final: {final_thread_count}"


def test_stress_task_and_scheduler_under_load():
    # Stress test: schedule multiple jobs and tasks under load and verify clean shutdown
    from sagittarius_engine import App
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )

    app = App(StdLibContainer(), MemoryEventBus())
    app.boot()

    task_run_count = 0
    lock = threading.Lock()

    def fast_task():
        nonlocal task_run_count
        with lock:
            task_run_count += 1

    # Spawn 100 fast concurrent background tasks
    for _ in range(100):
        app.context.tasks.spawn(fast_task)

    # Schedule 20 fast recurring jobs
    for i in range(20):
        app.context.scheduler.every(seconds=0.01).do(fast_task)

    # Let them run under load for 0.05 seconds
    time.sleep(0.05)

    # Stop the app gracefully
    app.stop()

    # The stopping sequence must cancel all tasks, stop the scheduler thread,
    # and complete currently executing tasks cleanly.
    assert app.context.lifecycle.is_stopped is True
    assert app.context.scheduler._thread is None
    assert app.context.async_runtime._thread is None


def test_benchmark_runnability():
    benchmark_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "benchmark_runtime.py")
    )
    assert os.path.exists(benchmark_path)
    run_example_script(benchmark_path)

