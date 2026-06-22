import asyncio
import unittest
from dataclasses import dataclass, field
from unittest.mock import MagicMock

from src.domain.event_bus import Event
from src.infrastructure.event_bus import InMemoryEventBus

@dataclass(frozen=True)
class TestEvent(Event):
    data: str = field(default="")

@dataclass(frozen=True)
class SubTestEvent(TestEvent):
    extra: str = field(default="")

class TestInMemoryEventBus(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bus = InMemoryEventBus()

    async def test_publish_subscribe_sync(self):
        # Arrange
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        event = TestEvent(data="test")

        # Act
        await self.bus.publish(event)

        # Assert
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    async def test_publish_subscribe_async(self):
        # Arrange
        received_events = []
        async def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        event = TestEvent(data="test")

        # Act
        await self.bus.publish(event)

        # Assert
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    async def test_unsubscribe(self):
        # Arrange
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, handler)
        self.bus.unsubscribe(TestEvent, handler)
        event = TestEvent(data="test")

        # Act
        await self.bus.publish(event)

        # Assert
        self.assertEqual(len(received_events), 0)

    async def test_inheritance_subscription(self):
        # Arrange
        received_events = []
        def handler(event: TestEvent):
            received_events.append(event)

        # Subscribe to base class
        self.bus.subscribe(TestEvent, handler)

        # Publish subclass event
        event = SubTestEvent(data="test", extra="extra")

        # Act
        await self.bus.publish(event)

        # Assert
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

    async def test_handler_error_does_not_stop_others(self):
        # Arrange
        received_events = []
        def failing_handler(event: TestEvent):
            raise Exception("Boom")

        def success_handler(event: TestEvent):
            received_events.append(event)

        self.bus.subscribe(TestEvent, failing_handler)
        self.bus.subscribe(TestEvent, success_handler)
        event = TestEvent(data="test")

        # Act
        await self.bus.publish(event)

        # Assert
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], event)

if __name__ == "__main__":
    unittest.main()
