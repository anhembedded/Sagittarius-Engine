import warnings

from sagittarius_engine.extensions.cqrs.commands import ICommand

# Emit deprecation warning when imported
warnings.warn(
    "Importing ICommand from sagittarius_engine.interfaces is deprecated. "
    "Use sagittarius_engine.extensions.cqrs instead.",
    DeprecationWarning,
    stacklevel=2,
)
