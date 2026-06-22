from src.domain.configuration.Configuration_api import ConfigPort, AppConfig
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra
from dataclasses import asdict

class LocalConfigAdapter(ConfigPort):
    def __init__(self, json_infra: JsonFileInfra, filepath: str = "config.json") -> None:
        self._json_infra = json_infra
        self._filepath = filepath

    def load(self) -> AppConfig:
        try:
            data = self._json_infra.read_json(self._filepath)
            return AppConfig(mode=data.get("mode", "debug"))
        except FileNotFoundError:
            # Fallback handled by Composition Root or here if preferred.
            # Domain dictates default in dataclass.
            return AppConfig()
        except Exception:
            return AppConfig()

    def save(self, config: AppConfig) -> None:
        data = asdict(config)
        self._json_infra.write_json(self._filepath, data)
