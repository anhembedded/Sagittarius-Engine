import inspect
from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

class DependencyResolutionError(Exception):
    pass

from src.application.container_port import IContainer

class Container(IContainer):
    def __init__(self) -> None:
        self._bindings: dict[type, type] = {}
        self._instances: dict[type, Any] = {}
        self._factories: dict[type, Callable] = {}

    def bind(self, abstract: type, concrete: type) -> None:
        self._bindings[abstract] = concrete

    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        if callable(instance_or_factory) and not isinstance(instance_or_factory, type):
            self._factories[abstract] = instance_or_factory
        else:
            self._instances[abstract] = instance_or_factory

    def resolve(self, abstract: type[T]) -> T:
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
