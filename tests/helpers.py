import unittest
from unittest.mock import Mock, call
from src.core import App, IEventBus
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.container = StdLibContainer()
        self.event_bus = MemoryEventBus()
        self.app = App(container=self.container, event_bus=self.event_bus)

class EventBusSpy:
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus
        self.emitted_events = []

        # Monkey patch emit
        self.original_emit = event_bus.emit

        def spy_emit(name, data=None):
            self.emitted_events.append((name, data))
            self.original_emit(name, data)

        event_bus.emit = spy_emit

    def assert_emitted(self, event_name: str, times: int = 1):
        count = sum(1 for name, _ in self.emitted_events if name == event_name)
        if count != times:
            raise AssertionError(f"Expected event '{event_name}' to be emitted {times} times, but was emitted {count} times.")

def assert_event_emitted(event_bus: IEventBus, event_name: str, times: int = 1):
    # This requires the event_bus to have a tracker.
    # We will assume tests use a tracked event bus or a fixture that tracks it.
    if hasattr(event_bus, 'emitted_events'):
        count = sum(1 for name, _ in event_bus.emitted_events if name == event_name)
        if count != times:
            raise AssertionError(f"Expected event '{event_name}' to be emitted {times} times, but was emitted {count} times.")
    else:
        raise ValueError("The provided event_bus does not have tracking enabled. Use the 'event_bus' fixture or EventBusSpy.")
