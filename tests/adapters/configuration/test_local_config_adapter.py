import pytest
from unittest.mock import MagicMock
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from application.configuration.Configuration_api import AppConfig, CONFIG_VALUE

def test_local_config_adapter_load_valid():
    mock_infra = MagicMock()
    mock_infra.read_json.return_value = {
        "mode": "production",
        "client_name": "MyClient"
    }

    adapter = LocalConfigAdapter(mock_infra)
    config = adapter.load("test_config.json")

    mock_infra.read_json.assert_called_once_with("test_config.json")
    assert config.mode == "production"
    assert config.client_name == "MyClient"

def test_local_config_adapter_load_invalid_keys_ignored():
    mock_infra = MagicMock()
    mock_infra.read_json.return_value = {
        "mode": "debug",
        "unknown_key": "some_value"
    }

    adapter = LocalConfigAdapter(mock_infra)
    config = adapter.load("test_config.json")

    assert config.mode == "debug"
    assert config.client_name is None  # default fallback

def test_local_config_adapter_load_failure_fallback():
    mock_infra = MagicMock()
    # If read_json raises an exception, the adapter should return default config
    mock_infra.read_json.side_effect = FileNotFoundError()

    adapter = LocalConfigAdapter(mock_infra)
    config = adapter.load("test_config.json")

    assert config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value
    assert config.client_name is None

def test_local_config_adapter_save():
    mock_infra = MagicMock()
    adapter = LocalConfigAdapter(mock_infra)

    config = AppConfig(mode="production", client_name="Test")
    adapter.save(config, "out_config.json")

    mock_infra.write_json.assert_called_once_with("out_config.json", {
        "mode": "production",
        "client_name": "Test"
    })
