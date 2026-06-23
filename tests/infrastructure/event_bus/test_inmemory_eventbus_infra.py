import pytest
from src.infrastructure.event_bus.InMemory_EventBus_infra import InMemoryEventBusInfra
from application.event_bus.EventBus_api import Event
from unittest.mock import MagicMock

class MockEvent(Event):
    def __init__(self, data: str):
        self.data = data

class AnotherMockEvent(Event):
    pass

def test_subscribe_and_publish():
    bus = InMemoryEventBusInfra()

    handled_events = []
    def handler(event: MockEvent):
        handled_events.append(event)

    bus.subscribe(MockEvent, handler)

    event = MockEvent("hello")
    bus.publish(event)

    assert len(handled_events) == 1
    assert handled_events[0].data == "hello"

def test_publish_unhandled_event():
    bus = InMemoryEventBusInfra()

    handled_events = []
    def handler(event: MockEvent):
        handled_events.append(event)

    bus.subscribe(MockEvent, handler)

    event = AnotherMockEvent()
    bus.publish(event)

    assert len(handled_events) == 0

def test_unsubscribe():
    bus = InMemoryEventBusInfra()

    handled_events = []
    def handler(event: MockEvent):
        handled_events.append(event)

    bus.subscribe(MockEvent, handler)
    bus.unsubscribe(MockEvent, handler)

    event = MockEvent("hello")
    bus.publish(event)

    assert len(handled_events) == 0

def test_handler_error_logged():
    mock_logger = MagicMock()
    bus = InMemoryEventBusInfra(logger=mock_logger)

    def handler(event: MockEvent):
        raise ValueError("Something went wrong")

    bus.subscribe(MockEvent, handler)

    event = MockEvent("hello")
    # Should catch the error and log it
    bus.publish(event)

    mock_logger.exception.assert_called_once()
