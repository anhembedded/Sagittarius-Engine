import unittest
from dataclasses import dataclass, field

from src.domain.event_bus.EventBus_api import Event
from src.infrastructure.event_bus.InMemory_EventBus_infra import InMemoryEventBusInfra

@dataclass(frozen=True)
class MockEvent(Event):
    data: str = field(default="")

@dataclass(frozen=True)
class SubTestEvent(MockEvent):
    extra: str = field(default="")

class TestInMemoryEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = InMemoryEventBusInfra()

    def test_publish_subscribe_sync(self):
        received_events = []
        def handler(event: MockEvent):
            received_events.append(event)

        self.bus.subscribe(MockEvent, handler)
        event = MockEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    def test_unsubscribe(self):
        received_events = []
        def handler(event: MockEvent):
            received_events.append(event)

        self.bus.subscribe(MockEvent, handler)
        self.bus.unsubscribe(MockEvent, handler)
        event = MockEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 0)

    def test_inheritance_subscription(self):
        received_events = []
        def handler(event: MockEvent):
            received_events.append(event)

        self.bus.subscribe(MockEvent, handler)
        event = SubTestEvent(data="test", extra="extra")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    def test_handler_error_does_not_stop_others(self):
        received_events = []
        def failing_handler(event: MockEvent):
            raise Exception("Boom")

        def success_handler(event: MockEvent):
            received_events.append(event)

        self.bus.subscribe(MockEvent, failing_handler)
        self.bus.subscribe(MockEvent, success_handler)
        event = MockEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

if __name__ == "__main__":
    unittest.main()
