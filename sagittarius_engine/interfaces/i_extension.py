from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext


class IExtension(ABC):
    """Interface for Sagittarius Engine Extensions."""

    @abstractmethod
    def register(self, context: "EngineContext") -> None:
        """
        @brief Called first when the extension is registered to bind dependencies.
        @param context The EngineContext instance.
        """
        ...

    @abstractmethod
    def boot(self, context: "EngineContext") -> None:
        """
        @brief Called after all extensions have been registered to trigger startup logic.
        @param context The EngineContext instance.
        """
        ...

    @abstractmethod
    def shutdown(self, context: "EngineContext") -> None:
        """
        @brief Called when the engine is stopping to release resources.
        @param context The EngineContext instance.
        """
        ...
