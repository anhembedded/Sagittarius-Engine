from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.extensions.health_check_query import HealthCheckQuery
from sagittarius_engine.domain.base_event import BaseEvent
from sagittarius_engine.interfaces.i_module import IModule


class HealthUpdatedEvent(BaseEvent):
    event_name = "health.updated"

    def __init__(self, status: dict[str, Any]) -> None:
        super().__init__()
        self.status: dict[str, Any] = status


class HealthModule(IModule):
    def register(self, context: 'EngineContext') -> None:
        pass


class HealthExtension(IExtension):
    """
    @brief Extension for Application Health Checks.
    """

    def register(self, context: "EngineContext") -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        context.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, context: "EngineContext") -> None:
        """@brief Boots the Health Extension."""
        pass

    def shutdown(self, context: "EngineContext") -> None:
        """@brief Shuts down the Health Extension."""
        pass
