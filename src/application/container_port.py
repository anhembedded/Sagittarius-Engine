from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

class IContainer(ABC):
    @abstractmethod
    def bind(self, abstract: type, concrete: type) -> None:
        ...

    @abstractmethod
    def singleton(self, abstract: type, instance_or_factory: Union[Any, Callable]) -> None:
        ...

    @abstractmethod
    def resolve(self, abstract: type[T]) -> T:
        ...
