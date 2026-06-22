import json
import os
from typing import Any, Dict

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

    def read_json(self, filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found at {filepath}")

        with open(filepath, 'r') as f:
            return json.load(f)

    def write_json(self, filepath: str, data: Dict[str, Any]) -> None:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
