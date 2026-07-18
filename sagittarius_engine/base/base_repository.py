import warnings

from sagittarius_engine.extensions.persistence.repository import BaseRepository

# Emit deprecation warning when imported
warnings.warn(
    "Importing BaseRepository from sagittarius_engine.base is deprecated. "
    "Use sagittarius_engine.extensions.persistence instead.",
    DeprecationWarning,
    stacklevel=2,
)
