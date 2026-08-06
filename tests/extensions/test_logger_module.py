from sagittarius_engine.kernel import App
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.interfaces import IConfig, ILogger
from sagittarius_engine.extensions.logger.logger_module import LoggerExtension
from sagittarius_engine.infrastructure.logging.logger_config import LoggerConfig
import logging


def test_logger_module_registers_logger():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container=container, event_bus=event_bus)

    extension = LoggerExtension()
    app.use(extension)

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

        def get_all(self):
            return {}

    container.singleton(IConfig, FakeConfig())

    extension = LoggerExtension()
    app.use(extension)

    logger = container.resolve(ILogger)
    assert logger is not None


# --- LoggerConfig tests ---


def test_logger_config__defaults():
    """LoggerConfig() with no args must have sensible defaults."""
    cfg = LoggerConfig()
    assert cfg.log_level == logging.INFO
    assert cfg.log_file is None
    assert cfg.viewer_enabled is False
    assert cfg.viewer_host == "localhost"
    assert cfg.viewer_port == 9999
    assert cfg.viewer_module == "sagittarius-app"


def test_logger_config__from_iconfig__reads_all_keys():
    """from_iconfig() must map all IConfig keys to LoggerConfig fields."""

    class FakeConfig(IConfig):
        _data = {
            "log.level": "DEBUG",
            "log.file": "app.log",
            "log.viewer.enabled": True,
            "log.viewer.host": "192.168.1.1",
            "log.viewer.port": 5000,
            "log.viewer.module": "my-app",
        }

        def get(self, key, default=None):
            return self._data.get(key, default)

        def set(self, key, value):
            pass

        def get_all(self):
            return self._data.copy()

    cfg = LoggerConfig.from_iconfig(FakeConfig())
    assert cfg.log_level == logging.DEBUG
    assert cfg.log_file == "app.log"
    assert cfg.viewer_enabled is True
    assert cfg.viewer_host == "192.168.1.1"
    assert cfg.viewer_port == 5000
    assert cfg.viewer_module == "my-app"


def test_logger_config__from_iconfig__unknown_level_falls_back_to_info():
    """An unrecognised log level string must fall back to INFO, not raise."""

    class FakeConfig(IConfig):
        def get(self, key, default=None):
            return "VERBOSE" if key == "log.level" else default

        def set(self, key, value):
            pass

        def get_all(self):
            return {}

    cfg = LoggerConfig.from_iconfig(FakeConfig())
    assert cfg.log_level == logging.INFO


def test_logger_config__is_frozen():
    """LoggerConfig must be immutable (frozen dataclass)."""
    cfg = LoggerConfig()
    try:
        cfg.log_level = logging.DEBUG  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"
    except Exception:
        pass  # expected
