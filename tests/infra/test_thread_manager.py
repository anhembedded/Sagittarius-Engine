import threading
import time

from src.infrastructure.thread_manager import ThreadManager

def test_thread_manager_submit_executes_task_and_returns_future():
    manager = ThreadManager(max_workers=2)

    def my_task(x, y):
        return x + y

    future = manager.submit(my_task, 3, 5)
    result = future.result(timeout=2)

    assert result == 8
    manager.shutdown(wait=True)

def test_thread_manager_max_workers_limits_parallel_execution():
    manager = ThreadManager(max_workers=2)

    # We will use events to block the first two threads
    event1 = threading.Event()
    event2 = threading.Event()

    task_started = [False, False, False]

    def blocking_task(index, event):
        task_started[index] = True
        if event:
            event.wait()

    # Submit tasks that will block
    manager.submit(blocking_task, 0, event1)
    manager.submit(blocking_task, 1, event2)

    # Wait for the first two to actually start
    time.sleep(0.05)

    assert task_started[0] is True
    assert task_started[1] is True

    # Submit a third task, which should NOT start because max_workers=2
    manager.submit(blocking_task, 2, None)

    time.sleep(0.05)
    assert task_started[2] is False

    # Unblock one task
    event1.set()

    # Now the third task should start
    time.sleep(0.05)
    assert task_started[2] is True

    # Cleanup
    event2.set()
    manager.shutdown(wait=True)

def test_thread_manager_shutdown_wait_true():
    manager = ThreadManager(max_workers=1)

    event = threading.Event()

    task_completed = False

    def long_task():
        nonlocal task_completed
        event.wait()
        task_completed = True

    manager.submit(long_task)

    # Shutdown in a separate thread so we can unblock the task
    def shutdown_thread():
        manager.shutdown(wait=True)

    shutdown_th = threading.Thread(target=shutdown_thread)
    shutdown_th.start()

    # Ensure shutdown has started waiting
    time.sleep(0.05)
    assert shutdown_th.is_alive() is True

    # Let the task finish
    event.set()

    shutdown_th.join(timeout=2)
    assert shutdown_th.is_alive() is False
    assert task_completed is True

def test_thread_manager_shutdown_wait_false():
    manager = ThreadManager(max_workers=1)

    event = threading.Event()

    task_completed = False

    def long_task():
        nonlocal task_completed
        event.wait()
        task_completed = True

    manager.submit(long_task)

    # Should not block
    manager.shutdown(wait=False)

    # The task should still be running because we didn't wait
    assert task_completed is False

    # Cleanup to not leak the thread
    event.set()
    # Wait a bit for the thread pool to actually finish the task in the background
    time.sleep(0.05)
    assert task_completed is True
