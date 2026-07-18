import warnings

from sagittarius_engine.extensions.cqrs.queries import IQuery

# Emit deprecation warning when imported
warnings.warn(
    "Importing IQuery from sagittarius_engine.interfaces is deprecated. "
    "Use sagittarius_engine.extensions.cqrs instead.",
    DeprecationWarning,
    stacklevel=2,
)
