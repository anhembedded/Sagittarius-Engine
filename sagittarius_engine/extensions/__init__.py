# Package namespace for Sagittarius extensions.

# CQRS
from .cqrs import ICommand, IQuery

# Audit
from .audit import AuditExtension, AuditService

# Persistence
from .persistence import (
    BaseRepository,
    ISession,
    SQLAlchemySessionAdapter,
    DatabaseExtension,
    SqlAlchemyExtension,
)

# Health
from .health.health_module import HealthExtension, HealthUpdatedEvent
from .health.health_check_query import HealthCheckQuery, HealthCheckDTO

# Logger
from .logger.logger_module import LoggerExtension

# Thread Manager
from .thread_manager.thread_manager_module import ThreadManagerModule

__all__ = [
    # CQRS
    "ICommand",
    "IQuery",
    # Audit
    "AuditExtension",
    "AuditService",
    # Persistence
    "BaseRepository",
    "ISession",
    "SQLAlchemySessionAdapter",
    "DatabaseExtension",
    "SqlAlchemyExtension",
    # Health
    "HealthExtension",
    "HealthCheckQuery",
    "HealthCheckDTO",
    "HealthUpdatedEvent",
    # Logger
    "LoggerExtension",
    # Thread Manager
    "ThreadManagerModule",
]
