import warnings
from sagittarius_engine.extensions.persistence.database_module import (
    DatabaseModule as DatabaseModule,
    DatabaseExtension as DatabaseExtension,
    SqlAlchemyExtension as SqlAlchemyExtension,
    SQLALCHEMY_INSTALLED as SQLALCHEMY_INSTALLED,
)

# Emit deprecation warning when imported
warnings.warn(
    "Importing DatabaseModule from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
