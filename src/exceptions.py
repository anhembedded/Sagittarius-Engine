class ModuleRegistrationError(Exception):
    """@brief Error raised when a module fails to register."""

    pass


class DependencyResolutionError(Exception):
    """@brief Error raised when the Container fails to resolve a dependency."""

    pass
