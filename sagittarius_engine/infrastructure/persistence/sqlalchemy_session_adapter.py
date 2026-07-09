import warnings
from sagittarius_engine.extensions.persistence.sqlalchemy_session_adapter import (
    SQLAlchemySessionAdapter,
)

# Emit deprecation warning when imported
warnings.warn(
    "Importing SQLAlchemySessionAdapter from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
