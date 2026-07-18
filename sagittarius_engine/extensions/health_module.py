from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.extensions.health_check_query import HealthCheckQuery
from sagittarius_engine.interfaces.i_extension import IExtension


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


class HealthModule(HealthExtension):
    """
    @brief Deprecated wrapper for HealthExtension.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        import warnings

        warnings.warn(
            "HealthModule is deprecated. Use HealthExtension instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
