from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


class IConfig(ABC):
    """
    @brief Interface for Configuration management.
    """

    @abstractmethod
    def get(self, key: str, default: T = None, cast: type[T] | None = None) -> T:
        """
        @brief Gets a configuration value with generic type inference and optional type casting.

        @param key The configuration key.
        @param default The default value if the key is not found.
        @param cast Optional target type to cast the configuration value.
        @return The configuration value as type T.
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
