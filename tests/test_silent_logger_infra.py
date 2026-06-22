from src.infrastructure.Silent_Logger_infra import SilentLogger

def test_silent_logger_methods():
    logger = SilentLogger()
    # Ensure calling these methods doesn't raise any exceptions
    logger.debug("test")
    logger.info("test")
    logger.warning("test")
    logger.error("test")
    logger.exception("test")
    logger.critical("test")
    # Since it's silent, we just verify it runs without error
    assert True
