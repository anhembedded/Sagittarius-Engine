from abc import ABC, abstractmethod
from typing import Any
from src.domain.configuration.Configuration_api import ConfigPort, AppConfig, CONFIG_KEY
from dataclasses import asdict

class JsonStoragePort(ABC):
    @abstractmethod
    def read_json(self, filepath: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def write_json(self, filepath: str, data: dict[str, Any]) -> None:
        pass


class LocalConfigAdapter(ConfigPort):
    def __init__(self, json_infra: JsonStoragePort) -> None:
        self._json_infra = json_infra

    def load(self, config_path: str) -> AppConfig:
        try:
            data = self._json_infra.read_json(config_path)
            if not isinstance(data, dict):
                return AppConfig()
            
            config_dict = {}
            for k, v in data.items():
                try:
                    config_key = CONFIG_KEY[k]
                    config_dict[config_key.value] = v
                except KeyError:
                    pass
            return AppConfig(**config_dict)
        except Exception:
            return AppConfig()

    def save(self, config: AppConfig, config_path: str) -> None:
        data = asdict(config)
        self._json_infra.write_json(config_path, data)
