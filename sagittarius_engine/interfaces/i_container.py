from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


class IContainer(ABC):
    """
    @brief Interface for the Dependency Injection Container.

    @details The Container manages the initialization and distribution of dependencies.
    Instead of manually instantiating classes (e.g., new ClassA()), the Container
    automatically resolves them.

    @par Tutorial / Usage Example:
    @code
    container = StdLibContainer()
    container.bind(IUserRepository, PostgresUserRepository)

    # Get an instance (Dependencies are automatically resolved if any)
    repo = container.resolve(IUserRepository)
    @endcode
    """

    @abstractmethod
    def bind(self, abstract: type[T], concrete: type[T]) -> None:
        """
        @brief Binds an Interface to a specific Implementation.
        @details A new instance is created every time it is resolved (Transient).

        @param abstract The interface or abstract class type.
        @param concrete The concrete class type to instantiate.
        """
        ...

    @abstractmethod
    def singleton(
        self,
        abstract: type[T],
        instance_or_factory: T | Callable[..., T] | type[T],
    ) -> None:
        """
        @brief Registers a Singleton.
        @details The instance is created once and reused for all subsequent resolve requests.

        @param abstract The interface or abstract class type.
        @param instance_or_factory The existing instance or a factory function.
        """
        ...

    @abstractmethod
    def resolve(self, abstract: type[T]) -> T:
        """
        @brief Resolves and returns an instance of the requested type.

        @param abstract The class type to resolve.
        @return An instance of the requested type.
        """
        ...
