import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces import IConfig


@dataclass(frozen=True)
class LoggerConfig:
    """
    @brief Immutable configuration for StdLogger.

    @details All fields have sensible defaults so StdLogger can work
    without any IConfig present (e.g. in tests or minimal setups).

    Severity order: DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)
    log_level acts as a MINIMUM threshold: records below this level are silently dropped,
    regardless of which method (info/debug/error) was called.
    """

    # Minimum severity threshold for the logger.
    # Example: log_level=INFO → debug() calls are silently dropped.
    log_level: int = logging.INFO

    # Optional path to a log file; None means file logging is disabled.
    log_file: str | None = None

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
            viewer_enabled=config.get("log.viewer.enabled", False),
            viewer_host=config.get("log.viewer.host", "localhost"),
            viewer_port=config.get("log.viewer.port", 9999),
            viewer_module=config.get("log.viewer.module", "sagittarius-app"),
        )
