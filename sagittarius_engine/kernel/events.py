from dataclasses import dataclass


@dataclass
class ExtensionInitializing:
    """Event emitted when an extension is about to initialize."""
    extension_name: str


@dataclass
class ExtensionStarted:
    """Event emitted when an extension has started."""
    extension_name: str


@dataclass
class ExtensionStopped:
    """Event emitted when an extension has stopped."""
    extension_name: str


@dataclass
class ExtensionDisposed:
    """Event emitted when an extension has been disposed."""
    extension_name: str
