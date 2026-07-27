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

    def get(self, key: str, default: Any = None, cast: type[Any] | None = None) -> Any:
        self._load()
        val = self._cache.get(key, default)
        if cast is not None and val is not None and not isinstance(val, cast):
            try:
                return cast(val)
            except (ValueError, TypeError):
                return val
        return val

    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        self._load()
        self._cache[key] = value
