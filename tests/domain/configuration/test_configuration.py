import unittest
from unittest.mock import patch, MagicMock
from src.domain.configuration.Configuration_api import AppConfig, ConfigManager, CONFIG_TYPE, CONFIG_KEY
from src.domain.configuration.Adapter import FileConfigManager

class TestDomainConfiguration(unittest.TestCase):

    def test_app_config_defaults(self):
        config = AppConfig()
        self.assertEqual(config.mode, CONFIG_TYPE.APP_MODE_DEBUG.value)
        self.assertIsNone(config.client_name)

    def test_app_config_custom(self):
        config = AppConfig(mode=CONFIG_TYPE.APP_MODE_PRODUCTION.value, client_name="test_client")
        self.assertEqual(config.mode, CONFIG_TYPE.APP_MODE_PRODUCTION.value)
        self.assertEqual(config.client_name, "test_client")

    @patch('src.domain.configuration.Adapter.JsonFileInfra')
    def test_file_config_manager(self, MockJsonFileInfra):
        # Mock the underlying infrastructure return value
        mock_infra = MockJsonFileInfra.return_value
        mock_infra.load_json.return_value = [
            {"key": "mode", "value": "production"},
            {"key": "client_name", "value": "test_client"}
        ]

        manager = FileConfigManager()
        result = manager.load_config_from_file("dummy_path.json")

        mock_infra.load_json.assert_called_once_with("dummy_path.json")
        self.assertEqual(len(result), 2)
        # Result uses its own imported CONFIG_KEY, check keys dynamically based on values to avoid Enum reference mismatches
        keys_0 = list(result[0].keys())
        keys_1 = list(result[1].keys())
        self.assertEqual(keys_0[0].value, "mode")
        self.assertEqual(result[0][keys_0[0]], "production")

        self.assertEqual(keys_1[0].value, "client_name")
        self.assertEqual(result[1][keys_1[0]], "test_client")

    @patch('src.domain.configuration.Adapter.FileConfigManager')
    def test_config_manager(self, MockFileConfigManager):
        # Mock FileConfigManager adapter
        mock_adapter = MockFileConfigManager.return_value
        expected_result = [{CONFIG_KEY.mode: "production"}]
        mock_adapter.load_config_from_file.return_value = expected_result

        config_manager = ConfigManager("dummy_config.json")
        result = config_manager.load_config()

        mock_adapter.load_config_from_file.assert_called_once_with("dummy_config.json")
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
