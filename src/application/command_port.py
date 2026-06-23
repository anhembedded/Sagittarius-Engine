from abc import ABC, abstractmethod
from typing import Any

class ICommand(ABC):
    @abstractmethod
    def execute(self, input_dto: dict | None) -> Any:
        ...
