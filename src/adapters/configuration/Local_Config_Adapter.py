from src.domain.configuration.Configuration_api import ConfigPort, AppConfig, CONFIG_KEY
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra
from dataclasses import asdict

class LocalConfigAdapter(ConfigPort):
    def __init__(self, json_infra: JsonFileInfra) -> None:
        self._json_infra = json_infra

    def load(self, filepath: str) -> AppConfig:
        try:
            data = self._json_infra.read_json(filepath)
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

    def save(self, config: AppConfig, filepath: str) -> None:
        data = asdict(config)
        self._json_infra.write_json(filepath, data)
