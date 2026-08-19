import logging

from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.infrastructure.logging.logger_config import TRACE, LoggerConfig
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.utils.null_logger import NullLogger


def test_trace_is_registered_one_level_below_debug():
    """TRACE isn't a standard Python logging level — StdLogger must have
    registered it (both the level-name mapping and the module attribute)
    the moment this module is imported, regardless of whether a StdLogger
    instance was ever constructed."""
    assert TRACE == 5
    assert TRACE < logging.DEBUG
    assert logging.getLevelName(TRACE) == "TRACE"
    assert logging.TRACE == TRACE  # type: ignore[attr-defined]


def test_logger_config_resolves_trace_from_config_string():
    """`"log.level": "TRACE"` must resolve to the real TRACE level, the
    same way the five standard names already do — this only works because
    `logging.TRACE` is set as a real module attribute, not just registered
    via addLevelName()."""
    cfg = LoggerConfig.from_iconfig(DictConfig({"log.level": "TRACE"}))
    assert cfg.log_level == TRACE


def test_std_logger_trace_emits_only_at_trace_threshold(capsys):
    logger_trace = StdLogger(DictConfig({"log.level": "TRACE"}))
    logger_trace.trace("trace line")
    assert "trace line" in capsys.readouterr().out

    logger_debug_only = StdLogger(DictConfig({"log.level": "DEBUG"}))
    logger_debug_only.trace("should not appear")
    assert "should not appear" not in capsys.readouterr().out


def test_std_logger_critical_emits(capsys):
    logger = StdLogger(DictConfig({"log.level": "INFO"}))
    logger.critical("fatal line")
    captured = capsys.readouterr().out
    assert "fatal line" in captured
    assert "CRITICAL" in captured


def test_null_logger_critical_and_trace_are_safe_no_ops():
    """Must not raise — NullLogger is used wherever no real IConfig/ILogger
    was resolvable (see test_core.py's fallback case)."""
    logger = NullLogger()
    logger.critical("ignored")
    logger.trace("ignored")
