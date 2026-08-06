from typing import Any
from sagittarius_engine.interfaces import IConfig
from sagittarius_engine.infrastructure.config.config_source import ConfigSource


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

    def load_json(self, filepath: str) -> "ConfigManager":
        """
        @brief Convenience method to add a JSON file source.
        @param filepath Path to the JSON configuration file.
        """
        from sagittarius_engine.infrastructure.config.json_source import JsonSource

        self.add_source(JsonSource(filepath))
        return self

    def load_env(self, prefix: str = "") -> "ConfigManager":
        """
        @brief Convenience method to add an environment variables source.
        @param prefix Optional environment variable prefix.
        """
        from sagittarius_engine.infrastructure.config.env_source import EnvSource

        self.add_source(EnvSource(prefix=prefix))
        return self

    def load_dict(self, data: dict[str, Any]) -> "ConfigManager":
        """
        @brief Convenience method to add a dictionary source.
        @param data Dictionary containing configuration.
        """
        from sagittarius_engine.infrastructure.config.dict_source import DictSource

        self.add_source(DictSource(data))
        return self

    @classmethod
    def from_json(cls, filepath: str) -> "ConfigManager":
        """
        @brief Factory method creating a ConfigManager initialized with a JSON file.
        @param filepath Path to the JSON configuration file.
        """
        return cls().load_json(filepath)

    def _load(self) -> None:
        """@brief Loads and merges configurations from all sources."""
        if self._loaded:
            return
        self._cache = {}
        for source in self._sources:
            try:
                data = source.read()
                self._cache.update(data)
            except Exception as e:
                import logging

                logging.getLogger(__name__).error(f"Config read error: {e}")
        self._loaded = True

    def get(self, key: str, default: Any = None, cast: type[Any] | None = None) -> Any:
        self._load()
        val = self._cache.get(key, default)
        if cast is not None and val is not None and not isinstance(val, cast):
            try:
                return cast(val)
            except (ValueError, TypeError):
                return val
        return val

    def get_all(self) -> dict[str, Any]:
        """
        @brief Gets the entire configuration dictionary.
        @return A dictionary containing all configuration key-value pairs.
        """
        self._load()
        return self._cache.copy()

    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        self._load()
        self._cache[key] = value
