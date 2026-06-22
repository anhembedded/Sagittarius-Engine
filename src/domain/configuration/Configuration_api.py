from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from enum import Enum


class CONFIG_VALUE(Enum):
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
    mode: str = CONFIG_VALUE.APP_MODE_DEBUG.value
    client_name: str | None = None


class ConfigPort(ABC):
    """Port (interface) for configuration adapters.

    Adapters implementing this port should provide load/save semantics for
    AppConfig objects.
    """
    @abstractmethod
    def load(self, config_path: str) -> AppConfig:
        raise NotImplementedError()

    @abstractmethod
    def save(self, config: AppConfig, config_path: str) -> None:
        raise NotImplementedError()


class ConfigManager:
    """High-level manager to load configuration from a file-backed adapter.
    """

    def __init__(self, config_adapter: ConfigPort):
        self.__file_manager = config_adapter

    def load_config(self, config_path: str) -> AppConfig:
        """Load configuration using the adapter.
        """
        return self.__file_manager.load(config_path)
