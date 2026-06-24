from datetime import datetime, timezone
from src.base_event import BaseEvent

def test_base_event_initialization():
    event = BaseEvent()

    assert event.event_id is not None
    assert isinstance(event.event_id, str)

    assert event.occurred_on is not None
    assert isinstance(event.occurred_on, datetime)
    assert event.occurred_on.tzinfo == timezone.utc

def test_base_event_to_dict():
    event = BaseEvent()

    data = event.to_dict()
    assert 'event_id' in data
    assert 'occurred_on' in data
    assert data['event_id'] == event.event_id
    assert data['occurred_on'] == event.occurred_on.isoformat()
