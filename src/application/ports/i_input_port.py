from abc import ABC, abstractmethod
from typing import Any


class IInputPort(ABC):
    """
    @brief Interface for receiving input data into the application.
    """

    @abstractmethod
    def receive(self) -> dict[str, Any]:
        """
        @brief Receives input and returns it as a dictionary.

        @return A dictionary containing the input data.
        """
        pass
