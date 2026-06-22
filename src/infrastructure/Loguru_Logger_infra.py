import sys
from typing import Any
from loguru import logger as loguru_logger

from src.domain.logger import Logger


class LoguruLogger(Logger):
    """
    Concrete implementation of the Logger interface using Loguru.
    This class configures terminal (stdout) output with colors and file output
    with rotation/retention, capturing log trace caller details via frame depth configuration.
    """

    def __init__(self, log_file: str = "app.log", level: str = "INFO") -> None:
        # Remove default loguru handler
        loguru_logger.remove()

        # Config console logging with vibrant, readable clean formatting
        loguru_logger.add(
            sys.stdout,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            backtrace=True,
            diagnose=True,
        )

        # Config rotating file logging
        loguru_logger.add(
            log_file,
            level=level,
            rotation="10 MB",
            retention="10 days",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            backtrace=True,
            diagnose=True,
        )

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).error(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).exception(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        loguru_logger.opt(depth=1).critical(message, *args, **kwargs)
