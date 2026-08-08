import unittest
from unittest.mock import MagicMock
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from src.domain.configuration.Configuration_api import AppConfig

class TestLocalConfigAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_json_infra = MagicMock()
        self.adapter = LocalConfigAdapter(json_infra=self.mock_json_infra, filepath="test_config.json")

    def test_load_success(self):
        self.mock_json_infra.read_json.return_value = {"mode": "production"}
        config = self.adapter.load()

        self.mock_json_infra.read_json.assert_called_once_with("test_config.json")
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.mode, "production")

    def test_load_file_not_found(self):
        self.mock_json_infra.read_json.side_effect = FileNotFoundError()
        config = self.adapter.load()

        self.mock_json_infra.read_json.assert_called_once_with("test_config.json")
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.mode, "debug") # Default value

    def test_load_general_exception(self):
        self.mock_json_infra.read_json.side_effect = Exception("Unknown Error")
        config = self.adapter.load()

        self.mock_json_infra.read_json.assert_called_once_with("test_config.json")
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.mode, "debug") # Default value

    def test_save_success(self):
        config = AppConfig(mode="production", client_name="test")
        self.adapter.save(config)

        self.mock_json_infra.write_json.assert_called_once_with("test_config.json", {"mode": "production", "client_name": "test"})

if __name__ == '__main__':
    unittest.main()
