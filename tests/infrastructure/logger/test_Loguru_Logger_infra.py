import pytest
from unittest.mock import patch

from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger

@pytest.fixture
def logger_instance():
    # Patch loguru.logger to avoid actual file I/O and stdout during tests
    with patch("src.infrastructure.logger.Loguru_Logger_infra.loguru_logger") as mock_logger:
        instance = LoguruLogger()
        yield instance, mock_logger

def test_loguru_debug(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.debug("test debug", "arg1")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.debug.assert_called_with("test debug", "arg1")

def test_loguru_info(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.info("test info")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.info.assert_called_with("test info")

def test_loguru_warning(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.warning("test warning")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.warning.assert_called_with("test warning")

def test_loguru_error(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.error("test error")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.error.assert_called_with("test error")

def test_loguru_exception(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.exception("test exception")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.exception.assert_called_with("test exception")

def test_loguru_critical(logger_instance):
    logger, mock_logger = logger_instance
    mock_opt = mock_logger.opt.return_value
    logger.critical("test critical")
    mock_logger.opt.assert_called_with(depth=1)
    mock_opt.critical.assert_called_with("test critical")
