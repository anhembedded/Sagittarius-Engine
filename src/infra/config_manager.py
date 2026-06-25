import os
import json
from abc import ABC, abstractmethod
from typing import Any
from src.interfaces import IConfig

class ConfigSource(ABC):
    """
    @brief Configuration Source (Dict, Env, Json).
    """
    @abstractmethod
    def read(self) -> dict[str, Any]:
        """
        @brief Reads the configuration from the source.
        @return A dictionary containing the configuration data.
        """
        ...

class DictSource(ConfigSource):
    """
    @brief Configuration source from a provided Python Dictionary.
    """
    def __init__(self, data: dict[str, Any]) -> None:
        """
        @brief Constructor.
        @param data The dictionary data.
        """
        self.data = data

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from the dictionary."""
        return self.data

class EnvSource(ConfigSource):
    """
    @brief Configuration source from Environment Variables.

    @details Example: EnvSource(prefix="APP_") will read the `APP_HOST` variable and store it with the key `HOST`.
    """
    def __init__(self, prefix: str = "") -> None:
        """
        @brief Constructor.
        @param prefix The prefix to filter environment variables by.
        """
        self.prefix = prefix

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from environment variables."""
        result = {}
        for k, v in os.environ.items():
            if k.startswith(self.prefix):
                key = k[len(self.prefix):]
                result[key] = v
        return result

class JsonSource(ConfigSource):
    """
    @brief Configuration source from a JSON file.
    """
    def __init__(self, filepath: str) -> None:
        """
        @brief Constructor.
        @param filepath The path to the JSON file.
        """
        self.filepath = filepath

    def read(self) -> dict[str, Any]:
        """@brief Reads the configuration from the JSON file."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

class ConfigManager(IConfig):
    """
    @brief Multi-layer configuration manager.

    @details Reads configurations from multiple sources and merges them.
    Sources added later will override the configurations of previously added sources.

    @par Tutorial / Usage Example:
    @code
    config = ConfigManager()

    # Add default JSON file
    config.add_source(JsonSource("default_config.json"))

    # Environment variables will override JSON configurations
    config.add_source(EnvSource(prefix="MYAPP_"))

    db_host = config.get("DB_HOST", "localhost")
    @endcode
    """
    def __init__(self) -> None:
        """@brief Constructor."""
        self._sources: list[ConfigSource] = []
        self._cache: dict[str, Any] = {}
        self._loaded = False

    def add_source(self, source: ConfigSource) -> None:
        """
        @brief Adds a configuration source to the manager.
        @param source The configuration source to add.
        """
        self._sources.append(source)
        self._loaded = False

    def _load(self) -> None:
        """@brief Loads and merges configurations from all sources."""
        if self._loaded:
            return
        self._cache = {}
        for source in self._sources:
            try:
                data = source.read()
                self._cache.update(data)
            except Exception:
                pass
        self._loaded = True

    def get(self, key: str, default: Any = None) -> Any:
        """
        @brief Gets a configuration value.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @return The configuration value.
        """
        self._load()
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        self._load()
        self._cache[key] = value
