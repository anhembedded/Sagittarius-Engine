from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


class TestMemoryEventBus:
    def test_memory_event_bus__off__removes_bound_method(self):
        bus = MemoryEventBus()
        event_name = "test_event"

        class DummyClass:
            def handle_event(self, data):
                pass

        obj = DummyClass()

        # Subscribe the bound method
        bus.on(event_name, obj.handle_event)

        # Verify it was added
        assert event_name in bus._handlers
        assert len(bus._handlers[event_name]) == 1
        assert obj.handle_event in bus._handlers[event_name]

        # Unsubscribe the bound method
        bus.off(event_name, obj.handle_event)

        # Verify it was removed
        assert event_name not in bus._handlers or len(bus._handlers[event_name]) == 0
