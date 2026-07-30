from abc import ABC, abstractmethod
from typing import Any
from sagittarius_engine.interfaces.i_event_bus import IEventBus
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_task_manager import ITaskManager


class ITaskCapability(ABC):
    """
    @brief Capability interface for background task management.
    """

    @property
    @abstractmethod
    def tasks(self) -> ITaskManager:
        ...


class ISchedulingCapability(ABC):
    """
    @brief Capability interface for task scheduling.
    """

    @property
    @abstractmethod
    def scheduler(self) -> Any:
        ...


class IEventCapability(ABC):
    """
    @brief Capability interface for event publishing and subscription.
    """

    @property
    @abstractmethod
    def event_bus(self) -> IEventBus:
        ...


class ILoggingCapability(ABC):
    """
    @brief Capability interface for application logging.
    """

    @property
    @abstractmethod
    def logger(self) -> ILogger | None:
        ...
