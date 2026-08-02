from abc import ABC, abstractmethod
from sagittarius_engine.interfaces.i_container import IContainer
from sagittarius_engine.interfaces.i_event_bus import IEventBus
from sagittarius_engine.interfaces.i_logger import ILogger
from sagittarius_engine.interfaces.i_task_manager import ITaskManager


class IEngineContext(ABC):
    """
    @brief Core Abstract Interface (Port) for the shared Engine Context.

    @details
    Clean Architecture Principle:
    According to the Dependency Inversion Principle (DIP), high-level modules
    (such as IHostedService or IExtension) must not depend on low-level concrete classes
    (like EngineContext in the kernel). Instead, both must depend on abstractions (this IEngineContext interface).

    By passing IEngineContext to Hosted Services and Extensions:
    - High-level components get full access to core engine ports (DI Container, EventBus, Logger, TaskManager).
    - IDEs can provide 100% accurate IntelliSense auto-completion.
    - Test suites can easily inject mock implementations of IEngineContext.
    """

    @property
    @abstractmethod
    def container(self) -> IContainer:
        """
        @brief The Dependency Injection Container interface.
        @return IContainer instance used for resolving registered dependencies.
        """
        ...

    @property
    @abstractmethod
    def event_bus(self) -> IEventBus:
        """
        @brief The Event Bus interface.
        @return IEventBus instance used for publishing and subscribing to events across modules.
        """
        ...

    @property
    @abstractmethod
    def logger(self) -> ILogger | None:
        """
        @brief The Logger interface if a logger is configured.
        @return ILogger instance or None if logging module is disabled.
        """
        ...

    @property
    @abstractmethod
    def tasks(self) -> ITaskManager:
        """
        @brief The Task Manager interface for spawning and managing background tasks.
        @return ITaskManager instance used for cooperative thread/coroutine execution.
        """
        ...
