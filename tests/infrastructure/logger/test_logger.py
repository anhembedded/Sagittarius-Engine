import unittest
from unittest.mock import MagicMock, patch
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger
from src.adapters.logger.Logger_adapter import Logger_Adapter
from src.infrastructure.logger.Silent_Logger__infra import SilentLoggerAdapter

class TestLogger(unittest.TestCase):
    def test_silent_logger_adapter(self) -> None:
        # Silent logger shouldn't raise any errors on any methods
        logger = SilentLoggerAdapter()
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.exception("test")
        logger.critical("test")

    @patch("src.infrastructure.logger.Loguru_Logger_infra.loguru_logger")
    def test_loguru_logger_adapter_delegation(self, mock_loguru: MagicMock) -> None:
        # Verify that LoguruLoggerAdapter passes calls down to LoguruLogger with correct stack depth
        infra = LoguruLogger()
        adapter = Logger_Adapter(infra)
        
        # Test info
        adapter.info("hello info")
        mock_loguru.opt.assert_called_with(depth=2)
        mock_loguru.opt().info.assert_called_with("hello info")

        # Test debug
        adapter.debug("hello debug")
        mock_loguru.opt.assert_called_with(depth=2)
        mock_loguru.opt().debug.assert_called_with("hello debug")
