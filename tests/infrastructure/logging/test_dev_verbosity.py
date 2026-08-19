import os
from datetime import UTC, datetime

from sagittarius_engine.infrastructure.logging.dev_verbosity import (
    resolve_dev_verbosity,
)

_FIXED_NOW = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)


def test_neither_flag_present_resolves_to_none(tmp_path):
    assert resolve_dev_verbosity([], str(tmp_path)) is None
    assert resolve_dev_verbosity(["main.py", "--other-flag"], str(tmp_path)) is None


def test_dev_flag_resolves_to_debug_level_and_dev_prefixed_file(tmp_path):
    result = resolve_dev_verbosity(["main.py", "--dev"], str(tmp_path), now=_FIXED_NOW)
    assert result is not None
    assert result.is_debug is False
    assert result.log_level == "DEBUG"
    assert os.path.basename(result.log_file) == "dev-20260102-030405.log"


def test_debug_flag_resolves_to_trace_level_and_debug_prefixed_file(tmp_path):
    result = resolve_dev_verbosity(
        ["main.py", "--debug"], str(tmp_path), now=_FIXED_NOW
    )
    assert result is not None
    assert result.is_debug is True
    assert result.log_level == "TRACE"
    assert os.path.basename(result.log_file) == "debug-20260102-030405.log"


def test_debug_flag_wins_when_both_are_present():
    """--debug implies --dev's own behavior plus more — passing both must
    not silently pick --dev's weaker DEBUG threshold."""
    result = resolve_dev_verbosity(["main.py", "--dev", "--debug"], "/tmp")
    assert result is not None
    assert result.is_debug is True
    assert result.log_level == "TRACE"


def test_creates_the_log_directory_if_missing(tmp_path):
    log_dir = tmp_path / "does" / "not" / "exist" / "yet"
    assert not log_dir.exists()

    resolve_dev_verbosity(["main.py", "--dev"], str(log_dir))

    assert log_dir.is_dir()
