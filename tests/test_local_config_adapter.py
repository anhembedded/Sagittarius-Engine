import pytest
from unittest.mock import MagicMock
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from src.domain.configuration.Configuration_api import AppConfig
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra

def test_local_config_adapter_load_success():
    infra_mock = MagicMock(spec=JsonFileInfra)
    infra_mock.read_json.return_value = {"mode": "release"}

    adapter = LocalConfigAdapter(infra_mock, "dummy.json")
    config = adapter.load()

    assert isinstance(config, AppConfig)
    assert config.mode == "release"
    infra_mock.read_json.assert_called_once_with("dummy.json")

def test_local_config_adapter_load_file_not_found():
    infra_mock = MagicMock(spec=JsonFileInfra)
    infra_mock.read_json.side_effect = FileNotFoundError()

    adapter = LocalConfigAdapter(infra_mock, "dummy.json")
    config = adapter.load()

    assert config.mode == "debug" # Default

def test_local_config_adapter_save():
    infra_mock = MagicMock(spec=JsonFileInfra)
    adapter = LocalConfigAdapter(infra_mock, "dummy.json")
    config = AppConfig(mode="release")

    adapter.save(config)

    infra_mock.write_json.assert_called_once_with("dummy.json", {"mode": "release"})
