import sys
from typing import Any
from loguru import logger as loguru_logger

from src.infrastructure.logger.Logger_abstract import LoggerAbstract_infr

class LoguruLogger(LoggerAbstract_infr):
    """
    Infrastructure class for Loguru. Handles initialization and raw logging calls.
    # Factory Pattern
    """

    def __init__(self, log_file: str = "app.log", level: str = "INFO") -> None:
        # Remove default loguru handler
        loguru_logger.remove()

        # Config console logging with vibrant, readable clean formatting
        # We format with {file.path}:{line}:{function} to allow VS Code terminal to resolve links
        loguru_logger.add(
            sys.stdout,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{file.path}:{line}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            backtrace=True,
            diagnose=True,
        )

        # Config rotating file logging
        loguru_logger.add(
            log_file,
            level=level,
            rotation="10 MB",
            retention="10 days",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {file.path}:{line}:{function} - {message}",
            backtrace=True,
            diagnose=True,
        )

    def debug(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).error(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).exception(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, depth: int = 1, **kwargs: Any) -> None:
        loguru_logger.opt(depth=depth).critical(message, *args, **kwargs)
