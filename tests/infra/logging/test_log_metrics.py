import json
import pytest
from unittest.mock import Mock
from sagittarius_engine.interfaces import ILogger
from sagittarius_engine.infrastructure.logging.log_metrics import LogMetrics

@pytest.fixture
def mock_logger():
    return Mock(spec=ILogger)

@pytest.fixture
def log_metrics(mock_logger):
    return LogMetrics(logger=mock_logger)

def test_log_metrics__set_gauge__without_tags(log_metrics, mock_logger):
    """Test set_gauge with no tags."""
    log_metrics.set_gauge("memory_usage", 1024.5)
    mock_logger.info.assert_called_once_with(
        "[METRIC] type=gauge name=memory_usage value=1024.5"
    )

def test_log_metrics__set_gauge__with_tags(log_metrics, mock_logger):
    """Test set_gauge with tags."""
    log_metrics.set_gauge("memory_usage", 1024.5, tags={"env": "prod", "region": "us-east-1"})
    expected_tags = ' ' + json.dumps({"env": "prod", "region": "us-east-1"})
    mock_logger.info.assert_called_once_with(
        f"[METRIC] type=gauge name=memory_usage value=1024.5{expected_tags}"
    )

def test_log_metrics__increment_counter__without_tags(log_metrics, mock_logger):
    """Test increment_counter with no tags and default value."""
    log_metrics.increment_counter("requests")
    mock_logger.info.assert_called_once_with(
        "[METRIC] type=counter name=requests value=1"
    )

def test_log_metrics__increment_counter__with_tags_and_value(log_metrics, mock_logger):
    """Test increment_counter with tags and custom value."""
    log_metrics.increment_counter("requests", value=5, tags={"status": "200"})
    expected_tags = ' ' + json.dumps({"status": "200"})
    mock_logger.info.assert_called_once_with(
        f"[METRIC] type=counter name=requests value=5{expected_tags}"
    )

def test_log_metrics__record_timing__without_tags(log_metrics, mock_logger):
    """Test record_timing with no tags."""
    log_metrics.record_timing("db_query", 45.2)
    mock_logger.info.assert_called_once_with(
        "[METRIC] type=timing name=db_query duration_ms=45.2"
    )

def test_log_metrics__record_timing__with_tags(log_metrics, mock_logger):
    """Test record_timing with tags."""
    log_metrics.record_timing("db_query", 45.2, tags={"table": "users"})
    expected_tags = ' ' + json.dumps({"table": "users"})
    mock_logger.info.assert_called_once_with(
        f"[METRIC] type=timing name=db_query duration_ms=45.2{expected_tags}"
    )
