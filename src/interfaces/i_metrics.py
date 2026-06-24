from abc import ABC, abstractmethod
from typing import Optional, Dict

class IMetrics(ABC):
    """
    @brief Interface for Application Metrics.

    @details Provides methods to record metrics such as counters, timings, and gauges.
    """

    @abstractmethod
    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Increments a counter metric.

        @param name The name of the metric.
        @param value The value to increment by.
        @param tags Optional tags/labels for the metric.
        """
        ...

    @abstractmethod
    def record_timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Records a timing/duration metric.

        @param name The name of the metric.
        @param duration_ms The duration in milliseconds.
        @param tags Optional tags/labels for the metric.
        """
        ...

    @abstractmethod
    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        @brief Sets a gauge metric to a specific value.

        @param name The name of the metric.
        @param value The value to set.
        @param tags Optional tags/labels for the metric.
        """
        ...
