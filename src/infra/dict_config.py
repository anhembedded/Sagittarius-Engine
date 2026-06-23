from typing import Any
from src.core import IConfig

class DictConfig(IConfig):
    def __init__(self) -> None:
        self._config: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
