from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.interfaces.i_engine_context import IEngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.extensions.health.health_check_query import HealthCheckQuery
from sagittarius_engine.domain.base_event import BaseEvent
from typing import Any


class HealthUpdatedEvent(BaseEvent):
    event_name = "health.updated"

    def __init__(self, status: dict[str, Any]) -> None:
        super().__init__()
        self.status: dict[str, Any] = status


class HealthExtension(IExtension):
    """
    @brief Extension for Application Health Checks.
    """

    def register(self, context: "IEngineContext") -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        context.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, context: "IEngineContext") -> None:
        """@brief Boots the Health Extension."""
        pass

    def shutdown(self, context: "IEngineContext") -> None:
        """@brief Shuts down the Health Extension."""
        pass
