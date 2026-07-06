from src.app_kernel import App
from src.infra.memory_event_bus import MemoryEventBus
from src.infra.std_container import StdLibContainer
from src.interfaces import IConfig, ILogger
from src.modules.logger_module import LoggerModule


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
