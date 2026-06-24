import pytest
from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus

class TrackedMemoryEventBus(MemoryEventBus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emitted_events = []

    def emit(self, event_name: str, data=None) -> None:
        self.emitted_events.append((event_name, data))
        super().emit(event_name, data)

@pytest.fixture
def container():
    return StdLibContainer()

@pytest.fixture
def event_bus():
    return TrackedMemoryEventBus()

@pytest.fixture
def app(container, event_bus):
    return App(container=container, event_bus=event_bus)
