from typing import Any, Callable

from attr import dataclass

from application.configuration.Configuration_api import AppConfig, ConfigManager, CONFIG_VALUE, ConfigPort
from application.logger.Logger_api import Logger

@dataclass(frozen=True)
class APP_DEFINITIONS:
    CONFIG_PATH = "config.json"

class AppManager:

    def __init__(self, config_adapter: ConfigPort):
        self.__config_adapter = config_adapter
        self.__AppConfig : AppConfig  # Placeholder for configuration instance
        self.__logger : Logger  # Placeholder for logger instance

    def __load_config(self) -> AppConfig:
        """
        Load configuration from a file or use default values.
        """
        config_manager: ConfigManager = ConfigManager(self.__config_adapter)
        return config_manager.load_config(APP_DEFINITIONS.CONFIG_PATH)

    def __wiring_components(self) -> None:
        """
        Wire up the components of the application based on the loaded configuration.
        (Wiring is pushed to Composition Root / adapters, AppManager manages state)
        """
        pass

    def __create_logger(self) -> Logger:
        """
        Create and configure the logger based on the application mode.
        """
        logger : Logger = Logger(config= self.__AppConfig)
        return logger


    def Bootstrap(self) -> None:
        """
        Bootstrap the application by loading configuration and initializing components.
        """
        self.__AppConfig = self.__load_config()
        self.__logger = self.__create_logger()
        self.__wiring_components()

    @property
    def logger(self) -> Logger:
        if self.__logger is None:
            raise RuntimeError("Logger is not initialized. Call Bootstrap() first.")
        return self.__logger

    @property
    def config(self) -> AppConfig:
        if self.__AppConfig is None:
            raise RuntimeError("Config is not initialized. Call Bootstrap() first.")
        return self.__AppConfig

