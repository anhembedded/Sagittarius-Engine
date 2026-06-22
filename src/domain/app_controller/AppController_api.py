from abc import ABC, abstractmethod

class IAppController(ABC):
    @abstractmethod
    def start(self) -> None:
        """Initialize the controller, subscribe to events"""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Cleanup subscriptions and gracefully shut down."""
        ...
