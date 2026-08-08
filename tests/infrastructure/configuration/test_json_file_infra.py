import unittest
import os
import tempfile
import json
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra

class TestJsonFileInfra(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test just in case
        JsonFileInfra._instance = None
        self.infra = JsonFileInfra()

    def test_singleton(self):
        infra1 = JsonFileInfra()
        infra2 = JsonFileInfra()
        self.assertIs(infra1, infra2)

    def test_read_write_json(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            filepath = tmp_file.name

        try:
            data_to_write = {"test_key": "test_value", "number": 42}

            # Write data
            self.infra.write_json(filepath, data_to_write)

            # Read data
            read_data = self.infra.read_json(filepath)
            self.assertEqual(read_data, data_to_write)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_read_json_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.infra.read_json("non_existent_file.json")

    def test_load_json(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            filepath = tmp_file.name

        try:
            data = {"mode": "production", "client_name": "test"}
            with open(filepath, 'w') as f:
                json.dump(data, f)

            result = self.infra.load_json(filepath)
            expected = [
                {"key": "mode", "value": "production"},
                {"key": "client_name", "value": "test"}
            ]
            self.assertEqual(result, expected)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_load_json_type_error(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            filepath = tmp_file.name

        try:
            # Write a list instead of a dict
            data = ["item1", "item2"]
            with open(filepath, 'w') as f:
                json.dump(data, f)

            with self.assertRaises(TypeError):
                self.infra.load_json(filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

if __name__ == '__main__':
    unittest.main()
