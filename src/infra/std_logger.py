import logging
import sys
from typing import Optional
from src.core import ILogger, IConfig

class StdLogger(ILogger):
    def __init__(self, config: Optional[IConfig] = None):
        self._logger = logging.getLogger("App")

        # Read configurations if IConfig is provided
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

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        # File handler (if configured)
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)
