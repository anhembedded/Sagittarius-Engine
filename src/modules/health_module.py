from typing import Any, Dict
from src.base_module import BaseModule
from src.app_kernel import App
from src.interfaces import IQuery, IContainer, IEventBus, ISession

class HealthCheckQuery(IQuery):
    """
    @brief Query to perform a health check on the application components.
    """
    def __init__(self, container: IContainer, event_bus: IEventBus):
        self.container = container
        self.event_bus = event_bus

    def execute(self, input_dto: Any = None) -> Dict[str, Any]:
        """
        @brief Executes the health check.
        @return A dictionary containing the health status of various components.
        """
        status = {
            "status": "healthy",
            "components": {
                "container": "ok",
                "event_bus": "ok",
                "database": "unknown"
            }
        }

        # Check Container
        try:
            self.container.resolve(IContainer)
        except Exception as e:
            status["components"]["container"] = f"error: {str(e)}"
            status["status"] = "unhealthy"

        # Check EventBus
        try:
            # We don't necessarily want to emit a real event if it has side effects,
            # but testing if emit is callable is a basic check.
            # Alternatively, test event_bus exists.
            if not hasattr(self.event_bus, 'emit'):
                raise ValueError("event_bus has no emit method")
        except Exception as e:
            status["components"]["event_bus"] = f"error: {str(e)}"
            status["status"] = "unhealthy"

        # Check Database
        try:
            session = self.container.resolve(ISession)
            # Try a simple query
            try:
                # E.g., for SQLAlchemy: execute("SELECT 1")
                # Using the adapter's execute method. The exact string depends on DB.
                # "SELECT 1" is fairly universal.
                from sqlalchemy import text
                session.execute(text("SELECT 1"))
                status["components"]["database"] = "ok"
            except ImportError as e:
                status["components"]["database"] = f"sqlalchemy not installed"
                status["status"] = "unhealthy"
            except Exception as e:
                status["components"]["database"] = f"error executing query: {str(e)}"
                status["status"] = "unhealthy"
        except Exception as e:
            status["components"]["database"] = f"not configured or resolving failed: {str(e)}"

        return status

class HealthModule(BaseModule):
    """
    @brief Module for Application Health Checks.

    @details Registers a HealthCheckQuery to allow monitoring systems to check application health.
    """

    def register(self, app: App) -> None:
        """@brief Registers the HealthCheckQuery in the container."""
        app.container.bind('health.check', HealthCheckQuery)

    def boot(self, app: App) -> None:
        """@brief Boots the Health Module."""
        pass
