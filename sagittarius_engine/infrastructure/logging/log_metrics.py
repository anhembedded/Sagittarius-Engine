import json

from sagittarius_engine.interfaces import ILogger
from sagittarius_engine.infrastructure.ports.i_metrics import IMetrics


class LogMetrics(IMetrics):
    """
    @brief Basic implementation of IMetrics that outputs metrics to the ILogger.
    """

    def __init__(self, logger: ILogger) -> None:
        """
        @brief Constructor.
        @param logger The logger instance to use for writing metrics.
        """
        self.logger = logger

    def _format_tags(self, tags: dict[str, str] | None) -> str:
        if not tags:
            return ""
        return " " + json.dumps(tags)

    def increment_counter(
        self, name: str, value: int = 1, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=counter name={name} value={value}{tag_str}")

    def record_timing(
        self, name: str, duration_ms: float, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(
            f"[METRIC] type=timing name={name} duration_ms={duration_ms}{tag_str}"
        )

    def set_gauge(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        tag_str = self._format_tags(tags)
        self.logger.info(f"[METRIC] type=gauge name={name} value={value}{tag_str}")
