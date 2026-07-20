import pytest
from sagittarius_engine.kernel.app import App
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor
from sagittarius_engine.interfaces.i_module import IModule
from sagittarius_engine.kernel.extension_manager import (
    create_module_extension_adapter,
    ModuleExtensionAdapter,
)
from sagittarius_engine.exceptions import (
    ExtensionDependencyError,
    ExtensionCircularDependencyError,
)
from sagittarius_engine.interfaces.events import (
    ExtensionInitializing,
    ExtensionStarted,
    ExtensionStopped,
    ExtensionDisposed,
)
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


class MockExtension(IExtension):
    def __init__(
        self,
        name: str,
        dependencies: list[str] = None,
        optional_dependencies: list[str] = None,
        priority: int = 0,
        enabled: bool = True,
        history: list = None,
    ):
        self._descriptor = ExtensionDescriptor(
            name=name,
            dependencies=dependencies or [],
            optional_dependencies=optional_dependencies or [],
            priority=priority,
            enabled=enabled,
        )
        self.initialized = False
        self.started = False
        self.stopped = False
        self.disposed = False
        self.history = history if history is not None else []

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._descriptor

    def register(self, context):
        self.initialized = True
        self.history.append(f"{self.descriptor.name}_initialized")

    def boot(self, context):
        self.started = True
        self.history.append(f"{self.descriptor.name}_started")

    def shutdown(self, context):
        self.stopped = True
        self.history.append(f"{self.descriptor.name}_stopped")

    def dispose(self, context):
        self.disposed = True
        self.history.append(f"{self.descriptor.name}_disposed")


def test_extension_manager_dependency_sorting():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    history = []
    ext_a = MockExtension("ExtA", dependencies=["ExtB"], history=history)
    ext_b = MockExtension("ExtB", history=history)

    # Registered in reverse dependency order
    app.use(ext_a)
    app.use(ext_b)

    app.boot()

    # B must start before A
    assert history.index("ExtB_initialized") < history.index("ExtA_initialized")
    assert history.index("ExtB_started") < history.index("ExtA_started")


def test_extension_manager_optional_dependency():
    # 1. Optional dependency is present
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    history = []
    ext_a = MockExtension("ExtA", optional_dependencies=["ExtB"], history=history)
    ext_b = MockExtension("ExtB", history=history)

    app.use(ext_a)
    app.use(ext_b)
    app.boot()

    assert history.index("ExtB_initialized") < history.index("ExtA_initialized")

    # 2. Optional dependency is missing (should boot normally)
    container2 = StdLibContainer()
    event_bus2 = MemoryEventBus()
    app2 = App(container2, event_bus2)

    ext_c = MockExtension("ExtC", optional_dependencies=["ExtD"])
    app2.use(ext_c)
    app2.boot()

    assert ext_c.initialized is True


def test_extension_manager_missing_dependency():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    ext_a = MockExtension("ExtA", dependencies=["ExtB"])
    app.use(ext_a)

    with pytest.raises(ExtensionDependencyError) as excinfo:
        app.boot()

    assert "requires missing dependency 'ExtB'" in str(excinfo.value)


def test_extension_manager_circular_dependency():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    ext_a = MockExtension("ExtA", dependencies=["ExtB"])
    ext_b = MockExtension("ExtB", dependencies=["ExtA"])

    app.use(ext_a)
    app.use(ext_b)

    with pytest.raises(ExtensionCircularDependencyError) as excinfo:
        app.boot()

    assert "Circular dependency detected" in str(excinfo.value)


def test_extension_manager_startup_rollback():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    history = []
    ext_a = MockExtension("ExtA", history=history)

    class FailingExtension(MockExtension):
        def register(self, context):
            raise RuntimeError("Initialization Failed")

    ext_b = FailingExtension("ExtB", dependencies=["ExtA"], history=history)

    app.use(ext_a)
    # B depends on A. A is initialized. When B is added, A is initialized, so B will try to initialize and fail.
    with pytest.raises(RuntimeError) as excinfo:
        app.use(ext_b)

    assert "Initialization Failed" in str(excinfo.value)

    # ExtA was initialized first, so it must be disposed on rollback
    assert ext_a.initialized is True
    assert ext_a.disposed is True

    # ExtB failed to initialize, so it shouldn't have been started
    assert ext_b.started is False


def test_extension_manager_shutdown_ordering():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    history = []
    ext_a = MockExtension("ExtA", dependencies=["ExtB"], history=history)
    ext_b = MockExtension("ExtB", history=history)

    app.use(ext_a)
    app.use(ext_b)
    app.boot()

    # Trigger shutdown/stop
    app.context.extension_manager.stop_and_dispose()

    # A must stop and dispose before B (reverse dependency order)
    assert history.index("ExtA_stopped") < history.index("ExtB_stopped")
    assert history.index("ExtA_disposed") < history.index("ExtB_disposed")


def test_extension_manager_lifecycle_events():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    emitted_events = []

    def on_event(event_name, event):
        emitted_events.append((event_name, event))

    event_bus.on("extension.initializing", lambda e: on_event("initializing", e))
    event_bus.on("extension.started", lambda e: on_event("started", e))

    ext_a = MockExtension("ExtA")
    app.use(ext_a)
    app.boot()

    assert len(emitted_events) == 2
    assert emitted_events[0][0] == "initializing"
    assert isinstance(emitted_events[0][1], ExtensionInitializing)
    assert emitted_events[0][1].extension_name == "ExtA"

    assert emitted_events[1][0] == "started"
    assert isinstance(emitted_events[1][1], ExtensionStarted)
    assert emitted_events[1][1].extension_name == "ExtA"


class DummyLegacyModule(IModule):
    def __init__(self):
        self.registered = False
        self.booted = False

    def register(self, app):
        self.registered = True

    def boot(self, app):
        self.booted = True

    def custom_method(self):
        return "custom"


def test_create_module_extension_adapter():
    legacy_module = DummyLegacyModule()
    adapter = create_module_extension_adapter(legacy_module)

    assert isinstance(adapter, ModuleExtensionAdapter)
    assert isinstance(adapter, IExtension)

    # Check class name is retained
    assert adapter.__class__.__name__ == "DummyLegacyModule"
    assert adapter.descriptor.name == "DummyLegacyModule"

    # Check register and boot
    class DummyApp:
        pass

    class DummyContext:
        def __init__(self):
            self.app = DummyApp()

    context = DummyContext()

    adapter.register(context)
    assert legacy_module.registered is True

    adapter.boot(context)
    assert legacy_module.booted is True

    # shutdown is a no-op but shouldn't fail
    adapter.shutdown(context)

    # Check __getattr__ delegation
    assert adapter.custom_method() == "custom"
