import os
import json
from abc import ABC, abstractmethod
from typing import Any
from src.core import IConfig

class ConfigSource(ABC):
    @abstractmethod
    def read(self) -> dict[str, Any]:
        ...

class DictSource(ConfigSource):
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def read(self) -> dict[str, Any]:
        return self.data

class EnvSource(ConfigSource):
    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix

    def read(self) -> dict[str, Any]:
        result = {}
        for k, v in os.environ.items():
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                result[key] = v
        return result

class JsonSource(ConfigSource):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

class ConfigManager(IConfig):
    def __init__(self) -> None:
        self._sources: list[ConfigSource] = []
        self._cache: dict[str, Any] = {}
        self._loaded = False

    def add_source(self, source: ConfigSource) -> None:
        self._sources.append(source)
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        self._cache = {}
        # Load sources in order, later sources override earlier ones
        for source in self._sources:
            data = source.read()
            self._cache.update(data)
        self._loaded = True

    def get(self, key: str, default: Any = None) -> Any:
        self._load()
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._load()
        self._cache[key] = value
