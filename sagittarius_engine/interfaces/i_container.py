from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Generator, TypeVar

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
    def bind(self, abstract: type[Any], concrete: type[Any]) -> None:
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
        abstract: type[Any],
        instance_or_factory: Any,
    ) -> None:
        """
        @brief Registers a Singleton.
        @details The instance is created once and reused for all subsequent resolve requests.

        @param abstract The interface or abstract class type.
        @param instance_or_factory The existing instance or a factory function.
        """
        ...

    @abstractmethod
    def resolve(self, abstract: type[Any]) -> Any:
        """
        @brief Resolves and returns an instance of the requested type.

        @param abstract The class type to resolve.
        @return An instance of the requested type.
        """
        ...

    @abstractmethod
    def scoped(self, abstract: type[Any], concrete: type[Any]) -> None:
        """
        @brief Registers a Scoped dependency.

        @details A scoped instance is created once per active scope (e.g., per HTTP request).
        Within the same scope, the same instance is returned. Different scopes receive
        different instances. If no scope is active, resolving a scoped dependency raises
        a DependencyResolutionError.

        @param abstract The abstract interface or class type.
        @param concrete The concrete class to instantiate within each scope.
        """
        ...

    @abstractmethod
    def create_scope(self) -> Any:
        """
        @brief Creates and returns a new dependency scope context manager.

        @details Use this as a context manager to define the boundary of a scope:

        @code
        with container.create_scope():
            session = container.resolve(ISession)  # scoped to this block
        @endcode

        @return A context manager (ScopeContext) that activates and deactivates the scope.
        """
        ...
