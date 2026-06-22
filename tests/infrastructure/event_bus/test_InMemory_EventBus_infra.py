import pytest
from dataclasses import dataclass
from unittest.mock import MagicMock

from src.domain.event_bus.EventBus_api import Event
from src.infrastructure.event_bus.InMemory_EventBus_infra import InMemoryEventBusInfra
from src.domain.logger.Logger_api import Logger

@dataclass(frozen=True)
class DummyEvent(Event):
    payload: str = ""

@dataclass(frozen=True)
class AnotherEvent(Event):
    value: int = 0

def test_subscribe_and_publish():
    bus = InMemoryEventBusInfra()
    received_events = []

    def handler(event: DummyEvent):
        received_events.append(event)

    bus.subscribe(DummyEvent, handler)

    event = DummyEvent(payload="test_payload")
    bus.publish(event)

    assert len(received_events) == 1
    assert received_events[0].payload == "test_payload"

def test_unsubscribe():
    bus = InMemoryEventBusInfra()
    received_events = []

    def handler(event: DummyEvent):
        received_events.append(event)

    bus.subscribe(DummyEvent, handler)
    bus.unsubscribe(DummyEvent, handler)

    event = DummyEvent(payload="test_payload")
    bus.publish(event)

    assert len(received_events) == 0

def test_publish_unhandled_event():
    bus = InMemoryEventBusInfra()
    received_events = []

    def handler(event: DummyEvent):
        received_events.append(event)

    bus.subscribe(DummyEvent, handler)

    another_event = AnotherEvent(value=42)
    bus.publish(another_event)

    assert len(received_events) == 0

def test_handler_exception_with_logger():
    mock_logger = MagicMock(spec=Logger)
    bus = InMemoryEventBusInfra(logger=mock_logger)

    def faulty_handler(event: DummyEvent):
        raise ValueError("Handler error")

    bus.subscribe(DummyEvent, faulty_handler)

    event = DummyEvent()
    bus.publish(event)

    mock_logger.exception.assert_called_once()
