import pytest

from src.infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter

def test_silent_logger():
    logger = SilentLoggerAdapter()

    # Should not raise any exceptions
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.exception("exception message")
    logger.critical("critical message")
