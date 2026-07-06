import pytest

from src.app_kernel import App
from src.infra.event_bus.memory_event_bus import MemoryEventBus
from src.infra.container.std_container import StdLibContainer
from src.infra.event_bus.thread_pool_event_bus import ThreadPoolEventBus
from src.infra.event_bus.ipc_queue_event_bus import IPCBroker, IPCQueueEventBus


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


@pytest.fixture
def thread_pool_bus_factory():
    buses = []

    def _factory(*args, **kwargs):
        bus = ThreadPoolEventBus(*args, **kwargs)
        buses.append(bus)
        return bus

    yield _factory

    for bus in buses:
        bus.shutdown()


@pytest.fixture
def ipc_broker_factory():
    brokers = []

    def _factory(*args, **kwargs):
        broker = IPCBroker(*args, **kwargs)
        brokers.append(broker)
        return broker

    yield _factory

    for broker in brokers:
        broker.stop()


@pytest.fixture
def ipc_bus_factory():
    buses = []

    def _factory(*args, **kwargs):
        bus = IPCQueueEventBus(*args, **kwargs)
        buses.append(bus)
        return bus

    yield _factory

    for bus in buses:
        bus.stop()
