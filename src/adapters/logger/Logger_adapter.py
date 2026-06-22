from typing import Any
from infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter
from src.domain.logger import Logger
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger
from domain.configuration.Configuration_api import AppConfig, CONFIG_TYPE
from src.infrastructure.logger.Logger_abstract import LoggerAbstract


class Logger_Adapter(LoggerAbstract):
    """
    Adapter pattern to translate Logger domain interface to Loguru infrastructure.
    # Adapter Pattern
    """

    def __init__(self, infra_logger: LoggerAbstract) -> None:
        self._infra = infra_logger

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.debug(message, *args, depth=2, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.info(message, *args, depth=2, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.warning(message, *args, depth=2, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.error(message, *args, depth=2, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.exception(message, *args, depth=2, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._infra.critical(message, *args, depth=2, **kwargs)

class LoggerAdapter_Factory:
    """
    Factory to create Logger instances based on AppConfig.
    # Factory Pattern
    """
    @staticmethod
    def create_logger(config: AppConfig) -> LoggerAbstract:
        if config.mode == CONFIG_TYPE.APP_MODE_DEBUG:
            infra_logger = LoguruLogger()
            return Logger_Adapter(infra_logger)
        else:
            infra_logger = SilentLoggerAdapter()
            return Logger_Adapter(infra_logger)