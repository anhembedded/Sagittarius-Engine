from unittest.mock import Mock

import pytest

from src.app_kernel import App
from src.base_module import BaseModule
from src.exceptions import ModuleRegistrationError
from src.infra.memory_event_bus import MemoryEventBus
from src.infra.std_container import DependencyResolutionError, StdLibContainer
from src.interfaces import ICommand, IEventBus, IQuery


def test_event_bus_emit_on_off():
    bus = MemoryEventBus()
    handler = Mock()

    bus.on("test_event", handler)
    bus.emit("test_event", {"data": "value"})
    handler.assert_called_once_with({"data": "value"})

    bus.off("test_event", handler)
    bus.emit("test_event", {"data": "value_2"})
    assert handler.call_count == 1  # Should not be called again


def test_container_singleton():
    container = StdLibContainer()

    class MyDependency:
        pass

    dep = MyDependency()
    container.singleton(MyDependency, dep)
    resolved = container.resolve(MyDependency)
    assert resolved is dep


def test_container_binding_resolution():
    container = StdLibContainer()

    class IService:
        pass

    class ServiceImpl(IService):
        pass

    container.bind(IService, ServiceImpl)
    resolved = container.resolve(IService)
    assert isinstance(resolved, ServiceImpl)


def test_container_auto_resolution():
    container = StdLibContainer()

    class Dependency:
        pass

    class Service:
        def __init__(self, dep: Dependency):
            self.dep = dep

    resolved = container.resolve(Service)
    assert isinstance(resolved, Service)
    assert isinstance(resolved.dep, Dependency)


def test_container_missing_typehint_fails():
    container = StdLibContainer()

    class BadService:
        def __init__(self, untyped_dep):
            pass

    with pytest.raises(DependencyResolutionError, match="Missing type hint"):
        container.resolve(BadService)


def test_app_use_module():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    class MyModule(BaseModule):
        def register(self, a: App):
            a.container.singleton("custom", "registered")

        def boot(self, a: App):
            pass

    module = MyModule()
    app.use(module)
    assert "custom" in app.container._instances
    assert app.container.resolve("custom") == "registered"


def test_app_use_invalid_module():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)
    with pytest.raises(ModuleRegistrationError):
        app.use(object())  # Not an IModule


def test_app_boot():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)
    handler = Mock()
    app.event_bus.on("app.booted", handler)

    boot_mock = Mock()

    class MyModule(BaseModule):
        def boot(self, a: App):
            boot_mock()

    app.use(MyModule())
    app.boot()

    boot_mock.assert_called_once()
    handler.assert_called_once_with(app)


def test_app_execute_command():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    class DummyCommand(ICommand):
        def __init__(self, event_bus: IEventBus):
            self.event_bus = event_bus

        def execute(self, input_dto: dict):
            return "executed"

    container.bind(DummyCommand, DummyCommand)
    container.singleton(IEventBus, event_bus)

    result = app.execute(DummyCommand, {})
    assert result == "executed"


def test_app_execute_query():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    class DummyQuery(IQuery):
        def __init__(self, event_bus: IEventBus):
            self.event_bus = event_bus

        def execute(self, input_dto: dict):
            return "queried"

    container.bind(DummyQuery, DummyQuery)
    container.singleton(IEventBus, event_bus)

    result = app.query(DummyQuery, {})
    assert result == "queried"
