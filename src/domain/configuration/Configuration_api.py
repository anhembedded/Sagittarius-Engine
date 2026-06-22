from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from enum import Enum


class CONFIG_TYPE(Enum):
    """Canonical configuration values used across the domain.
    Used by other modules (e.g. logger factory) to compare against values
    coming from AppConfig.
    """
    APP_MODE_DEBUG = "debug"
    APP_MODE_PRODUCTION = "production"


class CONFIG_KEY(Enum):
    """Keys used in configuration JSON files. Members' NAMES intentionally match
    the JSON keys so callers may index this Enum by the raw key string returned
    by infra helpers (e.g. JsonFileInfra.load_json -> items with "key").
    Example: CONFIG_KEY['mode'] -> CONFIG_KEY.mode
    """
    mode = "mode"
    client_name = "client_name"


@dataclass
class AppConfig:
    """Simple domain configuration object used across the application.

    Default values are domain-safe fallbacks.
    """
    mode: str = CONFIG_TYPE.APP_MODE_DEBUG.value
    client_name: Optional[str] = None


class ConfigPort(ABC):
    """Port (interface) for configuration adapters.

    Adapters implementing this port should provide load/save semantics for
    AppConfig objects.
    """
    @abstractmethod
    def load(self) -> AppConfig:
        raise NotImplementedError()

    @abstractmethod
    def save(self, config: AppConfig) -> None:
        raise NotImplementedError()


class ConfigManager:
    """High-level manager to load configuration from a file-backed adapter.

    This class avoids importing the concrete file adapter at module import
    time to prevent circular imports. The FileConfigManager (infra/adapter)
    is imported when an instance is created.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        # Local import to avoid circular import (Adapter imports this module)
        from src.domain.configuration.Adapter import FileConfigManager

        # FileConfigManager is an adapter around JsonFileInfra and exposes
        # `load_config_from_file(filepath)` returning list[dict[CONFIG_KEY, str]]
        self.__file_manager = FileConfigManager()

    def load_config(self) -> List[Dict[CONFIG_KEY, str]]:
        """Load raw key/value pairs from the configured JSON file and return
        them as a list of single-entry dicts keyed by CONFIG_KEY.
        """
        return self.__file_manager.load_config_from_file(self.config_path)
