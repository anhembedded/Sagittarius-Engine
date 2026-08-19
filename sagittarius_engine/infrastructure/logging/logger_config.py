import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces import IConfig

#: One level below DEBUG(10) — not a standard Python `logging` level, so it
#: must be registered explicitly. `logging.addLevelName()` only controls how
#: `%(levelname)s` renders a record; setting the `logging.TRACE` module
#: attribute is what lets `from_iconfig()`'s `getattr(logging, level_str)`
#: resolve `"log.level": "TRACE"` the same way it already resolves the five
#: standard names. Registered here, at this module's import time, rather
#: than in `std_logger.py`, so it exists the moment `LoggerConfig` itself is
#: imported — independent of whether `StdLogger` is ever constructed (e.g. a
#: `NullLogger`-only test that still sets `log.level=TRACE`).
TRACE = 5
logging.addLevelName(TRACE, "TRACE")
logging.TRACE = TRACE  # type: ignore[attr-defined]


@dataclass(frozen=True)
class LoggerConfig:
    """
    @brief Immutable configuration for StdLogger.

    @details All fields have sensible defaults so StdLogger can work
    without any IConfig present (e.g. in tests or minimal setups).

    Severity order: TRACE(5) < DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
    log_level acts as a MINIMUM threshold: records below this level are silently dropped,
    regardless of which method (trace/debug/info/warning/error/critical) was called.
    """

    # Minimum severity threshold for the logger.
    # Example: log_level=INFO → debug() calls are silently dropped.
    log_level: int = logging.INFO

    # Optional path to a log file; None means file logging is disabled.
    log_file: str | None = None

    # Enable console logging (stdout). Default is True.
    console_enabled: bool = True

    # TCP LogViewer settings — only active when viewer_enabled is True.
    viewer_enabled: bool = False
    viewer_host: str = "localhost"
    viewer_port: int = 9999
    viewer_module: str = "sagittarius-app"

    @staticmethod
    def from_iconfig(config: "IConfig") -> "LoggerConfig":
        """
        @brief Factory: parse LoggerConfig from an IConfig instance.

        @param config  An IConfig providing key/value access to application settings.
        @return        A fully populated, immutable LoggerConfig.
        """
        level_str: str = config.get("log.level", "INFO").upper()
        # getattr fallback ensures an unrecognised string (e.g. "VERBOSE") defaults to INFO.
        log_level: int = getattr(logging, level_str, logging.INFO)

        return LoggerConfig(
            log_level=log_level,
            log_file=config.get("log.file"),
            console_enabled=config.get("log.console.enabled", True),
            viewer_enabled=config.get("log.viewer.enabled", False),
            viewer_host=config.get("log.viewer.host", "localhost"),
            viewer_port=config.get("log.viewer.port", 9999),
            viewer_module=config.get("log.viewer.module", "sagittarius-app"),
        )
