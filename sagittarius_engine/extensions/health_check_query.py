from dataclasses import dataclass
from typing import Any
from sagittarius_engine.interfaces import IContainer, IEventBus, IQuery
from sagittarius_engine.infrastructure.persistence.i_session import ISession

@dataclass
class HealthCheckDTO:
    """
    @brief DTO for HealthCheckQuery.
    """
    pass

class HealthCheckQuery(IQuery):
    """
    @brief Query to perform a health check on the application components.
    """

    def __init__(self, container: IContainer, event_bus: IEventBus):
        self.container = container
        self.event_bus = event_bus

    def execute(self, input_dto: HealthCheckDTO | None=None) -> dict[str, Any]:
        """
        @brief Executes the health check.
        @return A dictionary containing the health status of various components.
        """
        status: dict[str, Any] = {'status': 'healthy', 'components': {'container': 'ok', 'event_bus': 'ok', 'database': 'unknown'}}
        try:
            self.container.resolve(IContainer)
        except Exception:
            status['components']['container'] = 'error: container resolution failed'
            status['status'] = 'unhealthy'
        try:
            if not hasattr(self.event_bus, 'emit'):
                raise ValueError('event_bus has no emit method')
        except Exception:
            status['components']['event_bus'] = 'error: event bus check failed'
            status['status'] = 'unhealthy'
        try:
            session: ISession = self.container.resolve(ISession)
            try:
                from sqlalchemy import text
                session.execute(text('SELECT 1'))
                status['components']['database'] = 'ok'
            except ImportError:
                status['components']['database'] = 'sqlalchemy not installed'
                status['status'] = 'unhealthy'
            except Exception:
                status['components']['database'] = 'database connection failed'
                status['status'] = 'unhealthy'
        except Exception:
            status['components']['database'] = 'not configured or resolving failed'
        return status
