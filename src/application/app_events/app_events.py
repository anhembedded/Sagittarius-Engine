from dataclasses import dataclass, field
from application.event_bus.EventBus_api import Event

@dataclass(frozen=True)
class StartPriceCommandEvent(Event):
    symbol: str = field(default="")

@dataclass(frozen=True)
class StopPriceCommandEvent(Event):
    symbol: str = field(default="")

@dataclass(frozen=True)
class QuitCommandEvent(Event):
    pass

@dataclass(frozen=True)
class PriceUpdatedEvent(Event):
    symbol: str = field(default="")
    price: float = field(default=0.0)
    volume: float = field(default=0.0)
