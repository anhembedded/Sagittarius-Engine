import inspect
from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

from src.core import DependencyResolutionError, IContainer

class StdLibContainer(IContainer):
    """
    @brief Dependency Injection Container using the Python Standard Library (`inspect`).

    @details Responsible for automatically resolving dependencies for classes.
    The Container reads Type Hints (Type Annotations) in the `__init__` method to know
    what dependencies a class requires, then automatically instantiates and injects them.

    @par Tutorial / Usage Example:
    @code
    container = StdLibContainer()

    # 1. Register a Singleton (A single shared instance)
    container.singleton(IEventBus, MemoryEventBus())

    # 2. Register a standard Binding (A new instance is created on each resolve)
    container.bind(IUserRepository, PostgresUserRepository)

    # 3. Use a factory function if initialization is complex
    def make_db(container):
        return DatabaseConnection(host="localhost")
    container.singleton(DatabaseConnection, make_db)

    # 4. Resolve (Automatic dependency injection)
    # If CommandA requires IUserRepository in __init__, the container will
    # automatically fetch PostgresUserRepository and pass it in.
    command = container.resolve(CommandA)
    @endcode
    """
    def __init__(self) -> None:
        self._bindings: dict[type, type] = {}
        self._instances: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}

    def bind(self, abstract: type, concrete: type) -> None:
        """
        @brief Registers a mapping between an Interface and a concrete Class (Transient).

        @param abstract The abstract interface or class.
        @param concrete The concrete class to bind.
        """
        self._bindings[abstract] = concrete

    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        """
        @brief Registers an existing instance or a Factory function (executed once).

        @param abstract The abstract interface or class.
        @param instance_or_factory The existing instance or factory function.
        """
        if callable(instance_or_factory) and not isinstance(instance_or_factory, type):
            self._factories[abstract] = instance_or_factory
        else:
            self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: type[T]) -> T:
        """
        @brief Resolves and retrieves an instance of the requested type.
        @details This function recursively resolves the entire dependency tree.

        @param abstract The class type to resolve.
        @return An instance of the requested type.
        @exception DependencyResolutionError If the container cannot resolve a dependency.
        """
        if abstract in self._instances:
            return self._instances[abstract]

        if abstract in self._factories:
            instance = self._factories[abstract](self)
            self._instances[abstract] = instance
            return instance

        concrete = self._bindings.get(abstract, abstract)

        if not inspect.isclass(concrete):
            raise DependencyResolutionError(f"Cannot resolve {abstract}")

        if getattr(concrete, "__abstractmethods__", None):
            raise DependencyResolutionError(f"Cannot instantiate abstract class {concrete}")

        if getattr(concrete, "__init__", None) is object.__init__:
            return concrete()

        try:
            signature = inspect.signature(concrete.__init__)
        except ValueError:
            return concrete()

        dependencies = {}
        for name, param in signature.parameters.items():
            if name == 'self' or name == 'args' or name == 'kwargs':
                continue
            if param.annotation == inspect.Parameter.empty:
                raise DependencyResolutionError(f"Missing type hint for parameter '{name}' in {concrete.__name__}")
            try:
                dependencies[name] = self.resolve(param.annotation)
            except Exception as e:
                raise DependencyResolutionError(f"Failed to resolve '{name}' for {concrete.__name__}: {str(e)}")

        instance = concrete(**dependencies)
        return instance
