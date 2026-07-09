from abc import ABC, abstractmethod
from typing import Any


class IHostedService(ABC):
    """
    @brief Interface for long-running engine components (Hosted Services).
    """

    @abstractmethod
    def start(self, context: Any) -> None:
        """
        @brief Starts the service.
        """
        pass

    @abstractmethod
    def stop(self, context: Any) -> None:
        """
        @brief Stops the service.
        """
        pass
