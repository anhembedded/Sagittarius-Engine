from cryptography.utils import Enum
from src.domain.configuration.Configuration_api import AppConfig, CONFIG_VALUE
from src.domain.logger.Logger_api import Logger
from src.adapters.logger.Logger_adapter import Logger_Adapter
from src.infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger

class Logger_Infra_Type(Enum):
    LOGURU = "loguru"
    SILENT = "silent"

class LoggerFactory:
    """
    Factory to create Logger instances based on AppConfig.
    # Factory Pattern
    """
    @staticmethod
    def create(config: AppConfig) -> Logger:
        if config.mode == CONFIG_VALUE.APP_MODE_DEBUG.value:
            infra_logger = LoguruLogger()
            return Logger_Adapter(infra_logger)
        elif config.mode == CONFIG_VALUE.APP_MODE_PRODUCTION.value:
            infra_logger = SilentLoggerAdapter()
            return Logger_Adapter(infra_logger)
        else:
            # Fallback
            infra_logger = LoguruLogger()
            return Logger_Adapter(infra_logger)
