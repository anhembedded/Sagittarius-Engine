from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


class IConfig(ABC):
    """
    @brief Interface for Configuration management.
    """

    @abstractmethod
    def get(self, key: str, default: Any = None, cast: type[T] | None = None) -> Any:
        """
        @brief Gets a configuration value with generic type inference and optional type casting.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @param cast Optional target type to cast the configuration value.
        @return The configuration value as type T.
        """
        ...

    @abstractmethod
    def get_all(self) -> dict[str, Any]:
        """
        @brief Gets the entire configuration dictionary.
        @return A dictionary containing all configuration key-value pairs.
        """
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        @brief Sets a configuration value.

        @param key The configuration key.
        @param value The configuration value to store.
        """
        ...
