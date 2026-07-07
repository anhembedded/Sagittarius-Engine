from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.app import App

from src.core.base_module import BaseModule
from src.modules.health_check_query import HealthCheckQuery

class HealthModule(BaseModule):
    """
    @brief Module for Application Health Checks.

    @details Registers a HealthCheckQuery to allow monitoring systems to check application health.
    """

    def register(self, app: 'App') -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        app.container.bind(HealthCheckQuery, HealthCheckQuery)

    def boot(self, app: 'App') -> None:
        """@brief Boots the Health Module."""
        pass
