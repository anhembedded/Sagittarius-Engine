from typing import TYPE_CHECKING
from typing import Protocol, Any
from sagittarius_engine.interfaces.i_container import IContainer

if TYPE_CHECKING:
    pass

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.extensions.health.health_check_query import HealthCheckQuery
from sagittarius_engine.domain.base_event import BaseEvent


class HealthUpdatedEvent(BaseEvent):
    event_name = "health.updated"

    def __init__(self, status: dict[str, Any]) -> None:
        super().__init__()
        self.status: dict[str, Any] = status


class IHealthContext(Protocol):
    @property
    def container(self) -> IContainer: ...


class HealthExtension(IExtension[IHealthContext]):
    """
    @brief Extension for Application Health Checks.
    """

    def register(self, context: IHealthContext) -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        context.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, context: IHealthContext) -> None:
        """@brief Boots the Health Extension."""
        pass

    def shutdown(self, context: IHealthContext) -> None:
        """@brief Shuts down the Health Extension."""
        pass
