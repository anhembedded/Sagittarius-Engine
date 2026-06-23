from abc import ABC, abstractmethod
from typing import Any

class IQuery(ABC):
    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        ...
