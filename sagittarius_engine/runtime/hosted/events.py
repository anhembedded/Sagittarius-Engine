from dataclasses import dataclass


@dataclass
class HostedServiceStarted:
    """Event emitted when a hosted service has started."""
    service_name: str


@dataclass
class HostedServiceStopped:
    """Event emitted when a hosted service has stopped."""
    service_name: str
