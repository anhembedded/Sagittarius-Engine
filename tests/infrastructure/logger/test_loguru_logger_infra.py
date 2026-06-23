import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger
from src.infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter

@patch("src.infrastructure.logger.Loguru_Logger_infra.loguru_logger")
def test_loguru_logger_initialization(mock_loguru):
    logger = LoguruLogger(log_file="test.log", level="DEBUG")

    mock_loguru.remove.assert_called_once()
    assert mock_loguru.add.call_count == 2  # console and file

@patch("src.infrastructure.logger.Loguru_Logger_infra.loguru_logger")
def test_loguru_logger_methods(mock_loguru):
    logger = LoguruLogger()

    # Mock the .opt() chain
    mock_opt = MagicMock()
    mock_loguru.opt.return_value = mock_opt

    logger.debug("debug message")
    mock_opt.debug.assert_called_once_with("debug message")

    logger.info("info message")
    mock_opt.info.assert_called_once_with("info message")

    logger.warning("warning message")
    mock_opt.warning.assert_called_once_with("warning message")

    logger.error("error message")
    mock_opt.error.assert_called_once_with("error message")

    logger.exception("exception message")
    mock_opt.exception.assert_called_once_with("exception message")

    logger.critical("critical message")
    mock_opt.critical.assert_called_once_with("critical message")

def test_silent_logger():
    logger = SilentLoggerAdapter()

    # Silent logger should do nothing and not raise any exceptions
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.exception("exception")
    logger.critical("critical")
