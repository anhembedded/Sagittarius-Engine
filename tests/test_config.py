import unittest
from unittest.mock import patch, MagicMock
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from application.configuration.Configuration_api import ConfigManager, AppConfig, CONFIG_VALUE
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra


class TestConfiguration(unittest.TestCase):
    def test_local_config_adapter_load_success(self) -> None:
        json_infra = MagicMock(spec=JsonFileInfra)
        json_infra.read_json.return_value = {
            "mode": "production",
            "client_name": "my_client",
            "invalid_key": "ignored"
        }
        
        adapter = LocalConfigAdapter(json_infra)
        config = adapter.load("dummy.json")
        
        json_infra.read_json.assert_called_once_with("dummy.json")
        self.assertEqual(config.mode, "production")
        self.assertEqual(config.client_name, "my_client")

    def test_local_config_adapter_load_default(self) -> None:
        json_infra = MagicMock(spec=JsonFileInfra)
        json_infra.read_json.return_value = {}
        
        adapter = LocalConfigAdapter(json_infra)
        config = adapter.load("dummy.json")
        
        self.assertEqual(config.mode, CONFIG_VALUE.APP_MODE_DEBUG.value)
        self.assertEqual(config.client_name, None)

    def test_local_config_adapter_load_exception(self) -> None:
        json_infra = MagicMock(spec=JsonFileInfra)
        json_infra.read_json.side_effect = FileNotFoundError()
        
        adapter = LocalConfigAdapter(json_infra)
        config = adapter.load("dummy.json")
        
        self.assertEqual(config.mode, CONFIG_VALUE.APP_MODE_DEBUG.value)
        self.assertEqual(config.client_name, None)

    def test_local_config_adapter_save(self) -> None:
        json_infra = MagicMock(spec=JsonFileInfra)
        adapter = LocalConfigAdapter(json_infra)
        
        config = AppConfig(mode="production", client_name="test_client")
        adapter.save(config, "dummy.json")
        
        json_infra.write_json.assert_called_once_with(
            "dummy.json",
            {"mode": "production", "client_name": "test_client"}
        )

    def test_config_manager_load(self) -> None:
        # Verify ConfigManager works and loads configuration using the injected adapter
        json_infra = MagicMock(spec=JsonFileInfra)
        json_infra.read_json.return_value = {"mode": "production"}
        adapter = LocalConfigAdapter(json_infra)
        config_manager = ConfigManager(adapter)
        config = config_manager.load_config("test_config.json")
        self.assertEqual(config.mode, "production")
