from typing import Any

from cryptography.utils import Enum
from src.infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger
from application.configuration.Configuration_api import AppConfig, CONFIG_VALUE
from src.infrastructure.logger.Logger_abstract import LoggerAbstract_infr

class Logger_Infra_Type(Enum):
    LOGURU = "loguru"
    SILENT = "silent"

class Logger_Adapter:
    """
    Adapter pattern to translate Logger domain interface to Loguru infrastructure.
    # Adapter Pattern
    """

    def __init__(self, infra_logger: LoggerAbstract_infr) -> None:
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
    Factory to create Logger instances based on Logger_Infra_Type.
    # Factory Pattern
    """
    @staticmethod
    def create(config: Logger_Infra_Type) -> Logger_Adapter:

        if config == Logger_Infra_Type.LOGURU:
            infra_logger : LoggerAbstract_infr = LoguruLogger()
            return Logger_Adapter(infra_logger)
        elif config == Logger_Infra_Type.SILENT:
            infra_logger : LoggerAbstract_infr = SilentLoggerAdapter()
            return Logger_Adapter(infra_logger)
        else:
            raise ValueError(f"Unsupported logger type: {config}")