from attr import dataclass
from typing import Callable

from src.domain.configuration.Configuration_api import AppConfig, ConfigManager, CONFIG_VALUE, ConfigPort
from src.domain.logger.Logger_api import Logger
@dataclass(frozen=True)
class APP_DEFINITIONS:
    CONFIG_PATH = "config.json"

class AppManager:

    def __init__(self, config_adapter: ConfigPort, logger_factory: Callable[[AppConfig], Logger]):
        self.__config_adapter = config_adapter
        self.__logger_factory = logger_factory
        self.__AppConfig : AppConfig  # Placeholder for configuration instance
        self.__logger : Logger  # Placeholder for logger instance

    def __load_config(self) -> AppConfig:
        """
        Load configuration from a file or use default values.
        """
        config_manager : ConfigManager = ConfigManager(self.__config_adapter)
        return config_manager.load_config(APP_DEFINITIONS.CONFIG_PATH)

    def __wiring_components(self) -> None:
        """
        Wire up the components of the application based on the loaded configuration.
        """
        # Placeholder for actual wiring logic
        pass

    def __create_logger(self) -> Logger:
        """
        Create and configure the logger based on the application mode.
        """
        return self.__logger_factory(self.__AppConfig)


    def Bootstrap(self) -> None:
        """
        Bootstrap the application by loading configuration and initializing components.
        """
        self.__AppConfig = self.__load_config()
        self.__logger = self.__create_logger()

        self.__wiring_components()