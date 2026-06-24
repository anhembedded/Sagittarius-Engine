import logging
import sys
from typing import Optional
from src.core import ILogger, IConfig

class StdLogger(ILogger):
    """
    @brief Implementation of ILogger using the default Python `logging` module.

    @details Automatically reads the IConfig (if provided) to set the log level and log file.

    @par Tutorial / Usage Example:
    @code
    config = DictConfig()
    config.set("log.level", "DEBUG")
    config.set("log.file", "app.log")

    logger = StdLogger(config)
    logger.info("System initializing")
    logger.error("DB connection error")
    @endcode
    """
    def __init__(self, config: Optional[IConfig] = None):
        """
        @brief Constructor.
        @param config Optional configuration instance.
        """
        self._logger = logging.getLogger("App")

        log_level = logging.INFO
        log_file = None

        if config:
            level_str = config.get("log.level", "INFO").upper()
            log_level = getattr(logging, level_str, logging.INFO)
            log_file = config.get("log.file")

        self._logger.setLevel(log_level)
        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

    def info(self, message: str) -> None:
        """
        @brief Logs an informational message.
        @param message The message to log.
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """
        @brief Logs a warning message.
        @param message The message to log.
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        @brief Logs an error message.
        @param message The message to log.
        """
        self._logger.error(message)

    def debug(self, message: str) -> None:
        """
        @brief Logs a debug message.
        @param message The message to log.
        """
        self._logger.debug(message)
