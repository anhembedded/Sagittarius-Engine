from src.adapters.logger.Logger_adapter import Logger_Adapter, LoggerAdapter_Factory, Logger_Infra_Type
from src.domain.configuration.Configuration_api import AppConfig, CONFIG_VALUE
from typing import Any

class Logger:
    """
    Core Domain Logger Interface. All methods accept standard message template
    with optional formatting (*args, **kwargs).
    """
    def __init__(self, config: AppConfig):
        if config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value:
            self.__logger_adapter = LoggerAdapter_Factory.create(Logger_Infra_Type.LOGURU)
        elif config.mode == CONFIG_VALUE.APP_MODE_PRODUCTION.value:
            self.__logger_adapter = LoggerAdapter_Factory.create(Logger_Infra_Type.SILENT)


    def debug(self, message: str, *args: Any, **kwargs: Any):
        self.__logger_adapter.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.__logger_adapter.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.__logger_adapter.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.__logger_adapter.error(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.__logger_adapter.exception(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.__logger_adapter.critical(message, *args, **kwargs)

