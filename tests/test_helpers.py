import pytest
from tests.helpers import assert_event_emitted

def test_helpers_assert_event_emitted(event_bus):
    event_bus.emit("test_event_1", {"data": 1})
    event_bus.emit("test_event_2", {"data": 2})
    event_bus.emit("test_event_1", {"data": 3})

    assert_event_emitted(event_bus, "test_event_1", times=2)
    assert_event_emitted(event_bus, "test_event_2", times=1)

    with pytest.raises(AssertionError):
        assert_event_emitted(event_bus, "test_event_1", times=1)

    with pytest.raises(AssertionError):
        assert_event_emitted(event_bus, "test_event_3", times=1)

    assert_event_emitted(event_bus, "test_event_3", times=0)
