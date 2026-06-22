import pytest
from src.domain.configuration.Configuration_api import (
    AppConfig,
    CONFIG_VALUE,
    ConfigPort,
    ConfigManager,
)

class MockConfigAdapter(ConfigPort):
    def __init__(self, mock_config: AppConfig):
        self.mock_config = mock_config
        self.saved_config = None
        self.saved_path = None
        self.loaded_path = None

    def load(self, config_path: str) -> AppConfig:
        self.loaded_path = config_path
        return self.mock_config

    def save(self, config: AppConfig, config_path: str) -> None:
        self.saved_config = config
        self.saved_path = config_path

def test_app_config_defaults():
    config = AppConfig()
    assert config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value
    assert config.client_name is None

def test_config_manager_load():
    mock_config = AppConfig(mode="test_mode", client_name="test_client")
    adapter = MockConfigAdapter(mock_config)
    manager = ConfigManager(adapter)

    loaded_config = manager.load_config("dummy/path.json")

    assert loaded_config.mode == "test_mode"
    assert loaded_config.client_name == "test_client"
    assert adapter.loaded_path == "dummy/path.json"
