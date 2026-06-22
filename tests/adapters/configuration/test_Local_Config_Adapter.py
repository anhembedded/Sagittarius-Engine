import pytest
from typing import Any
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter, JsonStoragePort
from src.domain.configuration.Configuration_api import AppConfig, CONFIG_VALUE

class MockJsonStorage(JsonStoragePort):
    def __init__(self, data: Any):
        self.data = data
        self.written_data = None
        self.written_filepath = None

    def read_json(self, filepath: str) -> dict[str, Any]:
        if isinstance(self.data, Exception):
            raise self.data
        return self.data

    def write_json(self, filepath: str, data: dict[str, Any]) -> None:
        self.written_filepath = filepath
        self.written_data = data

def test_local_config_adapter_load_valid():
    storage = MockJsonStorage({"mode": "production", "client_name": "MyClient"})
    adapter = LocalConfigAdapter(storage)

    config = adapter.load("test.json")

    assert config.mode == "production"
    assert config.client_name == "MyClient"

def test_local_config_adapter_load_invalid_type():
    storage = MockJsonStorage(["not", "a", "dict"])
    adapter = LocalConfigAdapter(storage)

    config = adapter.load("test.json")

    assert config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value
    assert config.client_name is None

def test_local_config_adapter_load_exception():
    storage = MockJsonStorage(Exception("File read error"))
    adapter = LocalConfigAdapter(storage)

    config = adapter.load("test.json")

    assert config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value
    assert config.client_name is None

def test_local_config_adapter_save():
    storage = MockJsonStorage({})
    adapter = LocalConfigAdapter(storage)
    config = AppConfig(mode="production", client_name="MyClient")

    adapter.save(config, "out.json")

    assert storage.written_filepath == "out.json"
    assert storage.written_data == {"mode": "production", "client_name": "MyClient"}
