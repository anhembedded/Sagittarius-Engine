from abc import ABC, abstractmethod
from typing import Any


class IOutputPort(ABC):
    """
    @brief Interface for presenting output data from the application.
    """

    @abstractmethod
    def present(self, result: Any) -> None:
        """
        @brief Presents the result.

        @param result The result to present.
        """
        pass

    @abstractmethod
    def present_error(self, error: Exception) -> None:
        """
        @brief Presents an error.

        @param error The exception to present.
        """
        pass
