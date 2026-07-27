import logging
import sys
from typing import Any

from sagittarius_engine.infrastructure.logging.tcp_log_viewer_handler import TcpLogViewerHandler
from sagittarius_engine.interfaces import IConfig, ILogger


class StdLogger(ILogger):
    """
    @brief Implementation of ILogger using the default Python `logging` module.

    @details Automatically reads the IConfig (if provided) to set log level, log file,
    and optional TcpLogViewerHandler to stream logs to Sagittarius LogViewer.
    """

    def __init__(self, config: IConfig | None = None):
        """
        @brief Constructor.
        @param config Optional configuration instance.
        """
        self._logger = logging.getLogger("App")

        log_level = logging.INFO
        log_file = None
        viewer_enabled = False
        viewer_host = "localhost"
        viewer_port = 9999
        viewer_module = "sagittarius-app"

        if config:
            level_str = config.get("log.level", "INFO").upper()
            log_level = getattr(logging, level_str, logging.INFO)
            log_file = config.get("log.file")
            viewer_enabled = config.get("log.viewer.enabled", False)
            viewer_host = config.get("log.viewer.host", "localhost")
            viewer_port = config.get("log.viewer.port", 9999)
            viewer_module = config.get("log.viewer.module", "sagittarius-app")

        self._logger.setLevel(log_level)

        for handler in list(self._logger.handlers):
            handler.close()
            self._logger.removeHandler(handler)

        self._logger.handlers.clear()
        self._logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        if viewer_enabled:
            vh = TcpLogViewerHandler(
                host=viewer_host,
                port=viewer_port,
                module_name=viewer_module,
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
