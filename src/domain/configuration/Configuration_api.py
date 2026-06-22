from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass(frozen=True)
class AppConfig:
    mode: str = "debug"

class ConfigPort(ABC):
    @abstractmethod
    def load(self) -> AppConfig: ...

    @abstractmethod
    def save(self, config: AppConfig) -> None: ...
