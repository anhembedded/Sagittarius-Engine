from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass(frozen=True)
class Ticker:
    symbol: str
    price: float
    volume: float

TickCallback = Callable[[Ticker], None]

class CryptoStreamPort(ABC):
    @abstractmethod
    def start_stream(self, symbol: str, on_tick: TickCallback) -> None:
        ...

    @abstractmethod
    def stop_stream(self, symbol: str) -> None:
        ...
