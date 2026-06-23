import unittest
from dataclasses import dataclass, field

from application.event_bus.EventBus_api import Event
from src.infrastructure.event_bus.InMemory_EventBus_infra import InMemoryEventBusInfra

@dataclass(frozen=True)
class TestEvent(Event):
    data: str = field(default="")

@dataclass(frozen=True)
class SubTestEvent(TestEvent):
    extra: str = field(default="")

class TestInMemoryEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = InMemoryEventBusInfra()

    def test_publish_subscribe_sync(self):
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        event = TestEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    def test_unsubscribe(self):
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        self.bus.unsubscribe(TestEvent, handler)
        event = TestEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 0)

    def test_inheritance_subscription(self):
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        event = SubTestEvent(data="test", extra="extra")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    def test_handler_error_does_not_stop_others(self):
        received_events = []
        def failing_handler(event: TestEvent):
            raise Exception("Boom")

        def success_handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, failing_handler)
        self.bus.subscribe(TestEvent, success_handler)
        event = TestEvent(data="test")

        self.bus.publish(event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

if __name__ == "__main__":
    unittest.main()
