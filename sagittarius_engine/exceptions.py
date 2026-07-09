class ModuleRegistrationError(Exception):
    """@brief Error raised when a module fails to register."""

    pass


class DependencyResolutionError(Exception):
    """@brief Error raised when the Container fails to resolve a dependency."""

    pass


class PathTraversalError(ValueError):
    """@brief Raised when a file path attempts to escape the allowed base directory."""

    pass


class ExtensionDependencyError(Exception):
    """@brief Error raised when a required extension dependency is missing."""

    pass


class ExtensionCircularDependencyError(ExtensionDependencyError):
    """@brief Error raised when a circular dependency is detected between extensions."""

    pass
