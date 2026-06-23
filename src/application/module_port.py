from abc import ABC, abstractmethod
from typing import Any

class IModule(ABC):
    @abstractmethod
    def register(self, app: Any) -> None:
        ...

    @abstractmethod
    def boot(self, app: Any) -> None:
        ...
