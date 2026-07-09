from sagittarius_engine.kernel import App
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.interfaces import IConfig, ILogger
from sagittarius_engine.extensions.logger_module import LoggerModule


def test_logger_module_registers_logger():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    module = LoggerModule()
    app.use(module)

    logger = container.resolve(ILogger)
    assert logger is not None
    assert hasattr(logger, "info")


def test_logger_module_with_config():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    class FakeConfig(IConfig):
        def get(self, key, default=None):
            return "DEBUG" if key == "log.level" else default

        def set(self, key, value):
            pass

    container.singleton(IConfig, FakeConfig())

    module = LoggerModule()
    app.use(module)

    logger = container.resolve(ILogger)
    assert logger is not None
