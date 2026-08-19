import os
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

#: Flags any app built on this engine can check argv for, in increasing
#: verbosity order. `--debug` is strictly more verbose than `--dev` — an app
#: session started with `--debug` should still get everything `--dev` turns
#: on (see `.agents/rules/logging-rule.md` §6 in the app repo), this module
#: only resolves the log-level/log-file half of that.
DEV_FLAG = "--dev"
DEBUG_FLAG = "--debug"


@dataclass(frozen=True)
class DevVerbosity:
    """What a `--dev`/`--debug` argv flag resolves to: which level threshold
    to log at, and which file to capture the whole session into. `is_debug`
    lets the caller print a message that names the mode it actually got."""

    is_debug: bool
    log_level: str
    log_file: str


def resolve_dev_verbosity(
    argv: Sequence[str], log_dir: str, *, now: datetime | None = None
) -> DevVerbosity | None:
    """
    @brief Resolves `--dev`/`--debug` in `argv` into a log level and a
    timestamped session log file path, creating `log_dir` if needed.
    @returns `None` if neither flag is present — the caller should leave
    logging at its configured default in that case.
    @details `--debug` implies `--dev` (checking for `--debug` alone would
    silently do nothing if a caller only ever passes `--dev`). Requiring a
    config edit to raise verbosity, then asking whoever hit the bug to copy
    console scrollback by hand, is how diagnostic detail gets lost from a
    bug report — this exists so any app on this engine gets "a dev session
    is captured to a file automatically" for free instead of reinventing it.
    """
    is_debug = DEBUG_FLAG in argv
    if not is_debug and DEV_FLAG not in argv:
        return None

    os.makedirs(log_dir, exist_ok=True)
    stamp = (now or datetime.now(UTC)).strftime("%Y%m%d-%H%M%S")
    prefix = "debug" if is_debug else "dev"
    log_file = os.path.join(log_dir, f"{prefix}-{stamp}.log")

    # TRACE (registered by StdLogger/LoggerConfig, one level below DEBUG) is
    # deliberately reserved for --debug only — per-frame/per-pixel detail
    # too high-frequency even for a normal --dev diagnostic session.
    log_level = "TRACE" if is_debug else "DEBUG"

    return DevVerbosity(is_debug=is_debug, log_level=log_level, log_file=log_file)
