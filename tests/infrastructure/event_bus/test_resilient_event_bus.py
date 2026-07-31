from unittest.mock import Mock

from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.event_bus.resilient_event_bus import (
    ResilientEventBus,
)


def test_resilient_event_bus_success():
    inner_bus = MemoryEventBus()
    bus = ResilientEventBus(inner_bus, max_retries=2)

    handler = Mock()
    bus.on("test", handler)
    bus.emit("test", "data")

    handler.assert_called_once_with("data")
    assert len(bus.get_dlq()) == 0


def test_resilient_event_bus_retry_success():
    inner_bus = MemoryEventBus()
    bus = ResilientEventBus(inner_bus, max_retries=2)

    attempts = 0

    def flaky_handler(data):
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("Flaky error")

    bus.on("test", flaky_handler)
    bus.emit("test", "data")

    assert attempts == 2
    assert len(bus.get_dlq()) == 0


def test_resilient_event_bus_fails_to_dlq():
    inner_bus = MemoryEventBus()
    bus = ResilientEventBus(inner_bus, max_retries=2)

    attempts = 0

    def failing_handler(data):
        nonlocal attempts
        attempts += 1
        raise ValueError("Persistent error")

    bus.on("test", failing_handler)
    bus.emit("test", "data")

    # 1 initial + 2 retries = 3 attempts
    assert attempts == 3
    dlq = bus.get_dlq()
    assert len(dlq) == 1
    assert dlq[0][0] == "test"
    assert dlq[0][1] == "data"
    assert dlq[0][2] == failing_handler
    assert isinstance(dlq[0][3], ValueError)


def test_resilient_event_bus_reprocess():
    inner_bus = MemoryEventBus()
    bus = ResilientEventBus(inner_bus, max_retries=1)

    fail = True

    def conditional_handler(data):
        if fail:
            raise ValueError("Error")

    bus.on("test", conditional_handler)
    bus.emit("test", "data")

    assert len(bus.get_dlq()) == 1

    # Simulate resolving the underlying cause of failure and reprocess
    fail = False
    bus.reprocess()

    assert len(bus.get_dlq()) == 0
