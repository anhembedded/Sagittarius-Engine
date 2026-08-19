import logging
import sys
from typing import Any

from sagittarius_engine.infrastructure.logging.logger_config import TRACE, LoggerConfig
from sagittarius_engine.infrastructure.logging.tcp_log_viewer_handler import (
    TcpLogViewerHandler,
)
from sagittarius_engine.interfaces import IConfig, ILogger


class StdLogger(ILogger):
    """
    @brief Implementation of ILogger using the default Python `logging` module.

    @details Accepts an optional IConfig; delegates all config-key parsing to
    LoggerConfig so this class stays focused on handler wiring only.
    """

    def __init__(self, config: IConfig | None = None):
        """
        @brief Constructor.
        @param config Optional configuration instance. Parsed via LoggerConfig.from_iconfig().
        """
        self._logger = logging.getLogger("App")

        # Parse all logger settings from IConfig via the dedicated config type.
        # Falls back to LoggerConfig defaults (INFO level, no file, viewer disabled)
        # when no IConfig is provided (e.g. in tests or minimal setups).
        cfg: LoggerConfig = (
            LoggerConfig.from_iconfig(config) if config else LoggerConfig()
        )

        # setLevel sets the MINIMUM threshold for this logger.
        # Calling info() labels the record as INFO; setLevel decides whether that level is allowed through.
        # These are independent: info() can still be silently filtered if threshold > INFO.
        self._logger.setLevel(cfg.log_level)

        for handler in list(self._logger.handlers):
            handler.close()
            self._logger.removeHandler(handler)

        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        if cfg.console_enabled:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)

        if cfg.log_file:
            fh = logging.FileHandler(cfg.log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        if cfg.viewer_enabled:
            vh = TcpLogViewerHandler(
                host=cfg.viewer_host,
                port=cfg.viewer_port,
                module_name=cfg.viewer_module,
            )
            self._logger.addHandler(vh)

    def _format_extra(self, extra: dict[str, Any] | None) -> dict[str, Any]:
        return {"extra": extra} if extra is not None else {}

    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs an informational message with optional structured metadata.
        """
        self._logger.info(message, extra=self._format_extra(extra))

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs a warning message with optional structured metadata.
        """
        self._logger.warning(message, extra=self._format_extra(extra))

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs an error message with optional structured metadata.
        """
        self._logger.error(message, extra=self._format_extra(extra))

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs a debug message with optional structured metadata.
        """
        self._logger.debug(message, extra=self._format_extra(extra))

    def critical(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs a critical message with optional structured metadata.
        """
        self._logger.critical(message, extra=self._format_extra(extra))

    def trace(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """
        @brief Logs a trace message with optional structured metadata.
        @details `Logger` has no built-in `.trace()` method (TRACE isn't a
        standard level) — routed through `.log(TRACE, ...)` instead, same
        as `.debug()` is really `.log(DEBUG, ...)` under the hood.
        """
        self._logger.log(TRACE, message, extra=self._format_extra(extra))
