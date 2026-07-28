from abc import ABC, abstractmethod
from typing import Any
from sagittarius_engine.interfaces.i_container import IContainer
from sagittarius_engine.interfaces.i_event_bus import IEventBus
from sagittarius_engine.interfaces.i_logger import ILogger


class IEngineContext(ABC):
    """
    @brief Interface for the shared Engine Context passed to Extensions and Hosted Services.
    """

    @property
    @abstractmethod
    def container(self) -> IContainer:
        """@brief The Dependency Injection Container."""
        ...

    @property
    @abstractmethod
    def event_bus(self) -> IEventBus:
        """@brief The Event Bus instance."""
        ...

    @property
    @abstractmethod
    def logger(self) -> ILogger | None:
        """@brief The Logger instance if available."""
        ...

    @property
    @abstractmethod
    def tasks(self) -> Any:
        """@brief The Task Manager for spawning background tasks."""
        ...
