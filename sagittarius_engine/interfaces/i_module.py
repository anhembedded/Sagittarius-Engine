from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel import App


class IModule(ABC):
    """
    @brief Interface for application Modules.

    @details A Module is an independent organizational unit (like a plugin) that can contain
    controllers, services, repositories, commands, queries, etc.

    @par Tutorial / Usage Example:
    @code
    # 1. Create a class inheriting from IModule (or BaseModule for convenience).
    # 2. Override the `register` method to bind dependencies into the Container.
    # 3. Override the `boot` method to listen for events or setup logic on startup.
    @endcode
    """

    @property
    def name(self) -> str:
        """
        @brief Return the module's name. Defaults to the class name.
        """
        return self.__class__.__name__

    @abstractmethod
    def register(self, app: "App") -> None:
        """
        @brief Called first when the module is added to the App.
        @details Used to register components (services, repositories) into the DI Container.

        @param app The current application instance.
        """
        ...

    @abstractmethod
    def boot(self, app: "App") -> None:
        """
        @brief Called after all modules have been registered.
        @details Used to initialize connections, register event listeners, etc.

        @param app The current application instance.
        """
        ...

    @abstractmethod
    def shutdown(self, app: "App") -> None:
        """
        @brief Called when the application is stopping.
        @details Used to cleanly release resources, stop background tasks, etc.

        @param app The current application instance.
        """
        ...
