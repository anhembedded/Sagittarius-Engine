import warnings
from sagittarius_engine.extensions.persistence.i_session import ISession as ISession

# Emit deprecation warning when imported
warnings.warn(
    "Importing ISession from sagittarius_engine.infrastructure.persistence is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
