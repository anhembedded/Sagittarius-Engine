from sagittarius_engine.domain import BaseEvent
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.domain.i_domain_event import IDomainEvent


class CustomDomainEvent(BaseEvent):
    def __init__(self, payload: str):
        super().__init__()
        self.payload = payload


def test_event_bus_routes_domain_event():
    event_bus = MemoryEventBus()
    received_events = []

    def handle_custom_event(event: CustomDomainEvent):
        received_events.append(event)

    # In Sagitarrius EventBus, we register by event name (string)
    event_bus.on("custom.domain.event", handle_custom_event)

    # Act
    event = CustomDomainEvent(payload="integration_test")

    # Assert event implements interface
    assert isinstance(event, IDomainEvent)
    assert hasattr(event, "event_id")
    assert hasattr(event, "occurred_on")

    # Emit event through bus passing event object as data payload
    event_bus.emit("custom.domain.event", event)

    # Assert bus routed event successfully
    assert len(received_events) == 1
    assert isinstance(received_events[0], CustomDomainEvent)
    assert received_events[0].payload == "integration_test"
    assert received_events[0].event_id == event.event_id
    assert received_events[0].occurred_on == event.occurred_on
