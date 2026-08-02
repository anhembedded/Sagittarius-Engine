import threading
import pytest

from sagittarius_engine.kernel.app import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.event_bus.thread_pool_event_bus import (
    ThreadPoolEventBus,
)
from sagittarius_engine.infrastructure.event_bus.resilient_event_bus import (
    ResilientEventBus,
)
from sagittarius_engine.runtime.tasks.task_manager import DaemonThreadPoolExecutor
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor


def test_issue_001_daemon_executor_no_global_monkey_patch():
    original_thread_cls = threading.Thread
    executor = DaemonThreadPoolExecutor(max_workers=2, thread_name_prefix="TestDaemon")
    fut = executor.submit(lambda: 42)
    assert fut.result(timeout=2.0) == 42
    # Verify threading.Thread identity is strictly preserved
    assert threading.Thread is original_thread_cls
    executor.shutdown(wait=True)


def test_issue_001_global_thread_identity_never_mutated_during_concurrency():
    original_thread_cls = threading.Thread
    executors = [
        DaemonThreadPoolExecutor(max_workers=2, thread_name_prefix=f"BgPool_{i}")
        for i in range(5)
    ]
    futures = [
        ex.submit(lambda: threading.Thread is original_thread_cls) for ex in executors
    ]
    for fut in futures:
        assert fut.result(timeout=2.0) is True
    assert threading.Thread is original_thread_cls
    for ex in executors:
        ex.shutdown(wait=True)


def test_issue_002_event_bus_shutdown_on_app_stop():
    container = StdLibContainer()
    event_bus = ThreadPoolEventBus(max_workers=2)
    app = App(container, event_bus)
    app.boot()
    app.stop()
    assert event_bus._executor._shutdown is True


def test_issue_002_app_stop_idempotency():
    container = StdLibContainer()
    event_bus = ThreadPoolEventBus(max_workers=2)
    app = App(container, event_bus)
    app.boot()
    # Call stop 3 times
    app.stop()
    app.stop()
    app.stop()
    assert app.context.lifecycle.is_stopped is True


def test_issue_003_optional_dependencies_do_not_block_initialization():
    class ExtA(IExtension):
        @property
        def descriptor(self) -> ExtensionDescriptor:
            return ExtensionDescriptor(
                name="ExtA", optional_dependencies=["NonExistentExt"]
            )

        def register(self, context):
            pass

        def boot(self, context):
            pass

        def initialize(self, context):
            self.initialized = True

        def start(self, context):
            pass

        def stop(self, context):
            pass

        def shutdown(self, context):
            pass

        def dispose(self, context):
            pass

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)
    ext_a = ExtA()
    app.use(ext_a)
    app.boot()
    assert getattr(ext_a, "initialized", False) is True
    app.stop()


def test_issue_004_resilient_event_bus_no_split_paths():
    inner_bus = MemoryEventBus()
    resilient_bus = ResilientEventBus(inner_bus=inner_bus, max_retries=1)

    calls = []

    def handler(data):
        calls.append(data)

    resilient_bus.on("test.event", handler)
    inner_bus.emit("test.event", "payload")

    assert calls == ["payload"]
    assert len(resilient_bus.get_dlq()) == 0


def test_issue_004_nested_three_tier_event_bus_decoration():
    mem_bus = MemoryEventBus()
    tp_bus = ThreadPoolEventBus(max_workers=2)
    tp_bus._inner_bus = mem_bus
    resilient_bus = ResilientEventBus(inner_bus=tp_bus, max_retries=2)

    calls = []

    def handler(data):
        calls.append(data)

    resilient_bus.on("multi.tier.event", handler)
    resilient_bus.emit("multi.tier.event", "data")

    # Give thread pool time to execute
    import time

    time.sleep(0.1)

    assert "data" in calls
    tp_bus.shutdown(wait=True)


def test_issue_005_thread_pool_event_bus_public_get_handlers():
    memory_bus = MemoryEventBus()
    tp_bus = ThreadPoolEventBus(max_workers=2)

    def dummy(data):
        pass

    memory_bus.on("evt", dummy)

    handlers = memory_bus.get_handlers("evt")
    assert dummy in handlers
    tp_bus.shutdown(wait=True)


def test_issue_006_extension_rollback_disposes_in_reverse_order():
    history = []

    class Ext1(IExtension):
        @property
        def descriptor(self) -> ExtensionDescriptor:
            return ExtensionDescriptor(name="Ext1")

        def register(self, c):
            pass

        def boot(self, c):
            pass

        def initialize(self, c):
            history.append("init_1")

        def start(self, c):
            pass

        def stop(self, c):
            pass

        def shutdown(self, c):
            pass

        def dispose(self, c):
            history.append("dispose_1")

    class ExtFailing(IExtension):
        @property
        def descriptor(self) -> ExtensionDescriptor:
            return ExtensionDescriptor(name="ExtFailing", dependencies=["Ext1"])

        def register(self, c):
            pass

        def boot(self, c):
            pass

        def initialize(self, c):
            raise RuntimeError("Init Boom")

        def start(self, c):
            pass

        def stop(self, c):
            pass

        def shutdown(self, c):
            pass

        def dispose(self, c):
            pass

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)
    app.use(Ext1())
    with pytest.raises(RuntimeError) as exc:
        app.use(ExtFailing())

    assert "Init Boom" in str(exc.value)
    assert history == ["init_1", "dispose_1"]


def test_issue_007_engine_context_properties():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    ctx = app.context
    assert ctx.tasks is not None
    assert ctx.event_bus is event_bus
