import json
import os
from typing import Any

class JsonFileInfra:
    """
    Handles low-level reading and writing of JSON files.
    # Singleton Pattern
    """
    _instance = None

    def __new__(cls) -> 'JsonFileInfra':
        if cls._instance is None:
            cls._instance = super(JsonFileInfra, cls).__new__(cls)
        return cls._instance

    def read_json(self, filepath: str) -> dict[str, Any]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found at {filepath}")

        with open(filepath, 'r') as f:
            return json.load(f)

    def write_json(self, filepath: str, data: dict[str, Any]) -> None:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def load_json(self, filepath: str) -> list[dict[str, Any]]:
        """
        Load a JSON file and return a list of key/value dicts for top-level mapping.

        Example: if file contains {"a": 1, "b": 2} this returns
        [{"key": "a", "value": 1}, {"key": "b", "value": 2}]
        """
        data = self.read_json(filepath)

        if isinstance(data, dict):
            return [{"key": k, "value": v} for k, v in data.items()]

        raise TypeError(f"Expected top-level JSON object (dict) in {filepath}, got {type(data).__name__}")

    
