import warnings

from sagittarius_engine.extensions.persistence.database_module import (
    SQLALCHEMY_INSTALLED,
    DatabaseExtension,
    DatabaseModule,
    SqlAlchemyExtension,
)

# Emit deprecation warning when imported
warnings.warn(
    "Importing DatabaseModule from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
