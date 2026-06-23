import pytest
from src.domain.configuration.Configuration_api import ConfigPort, AppConfig, ConfigManager, CONFIG_VALUE, CONFIG_KEY

class MockConfigAdapter(ConfigPort):
    def __init__(self):
        self.loaded_filepath = None
        self.saved_filepath = None
        self.saved_config = None

    def load(self, filepath: str) -> AppConfig:
        self.loaded_filepath = filepath
        return AppConfig(mode=CONFIG_VALUE.APP_MODE_PRODUCTION.value, client_name="test_client")

    def save(self, config: AppConfig, filepath: str) -> None:
        self.saved_config = config
        self.saved_filepath = filepath

def test_app_config_defaults():
    config = AppConfig()
    assert config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value
    assert config.client_name is None

def test_config_manager_load():
    adapter = MockConfigAdapter()
    manager = ConfigManager(adapter)

    config = manager.load_config("dummy/path.json")

    assert adapter.loaded_filepath == "dummy/path.json"
    assert config.mode == CONFIG_VALUE.APP_MODE_PRODUCTION.value
    assert config.client_name == "test_client"

def test_config_enums():
    assert CONFIG_VALUE.APP_MODE_DEBUG.value == "debug"
    assert CONFIG_VALUE.APP_MODE_PRODUCTION.value == "production"

    assert CONFIG_KEY.mode.value == "mode"
    assert CONFIG_KEY.client_name.value == "client_name"
