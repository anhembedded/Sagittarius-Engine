from abc import ABC, abstractmethod
from typing import Any

class ConfigSource(ABC):
    """
    @brief Configuration Source (Dict, Env, Json).
    """

    @abstractmethod
    def read(self) -> dict[str, Any]:
        """
        @brief Reads the configuration from the source.
        @return A dictionary containing the configuration data.
        """
        ...
