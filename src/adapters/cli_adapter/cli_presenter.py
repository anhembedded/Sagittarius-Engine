from src.domain.event_bus.EventBus_api import EventBus
from src.domain.app_events.app_events import StartPriceCommandEvent, StopPriceCommandEvent, QuitCommandEvent

class CLIPresenter:
    """
    Acts as an Input Adapter. Translates raw CLI interactions into Application Domain Events.
    """
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    def publish_start_price(self, symbol: str) -> None:
        self._event_bus.publish(StartPriceCommandEvent(symbol=symbol))

    def publish_stop_price(self, symbol: str) -> None:
        self._event_bus.publish(StopPriceCommandEvent(symbol=symbol))

    def publish_quit(self) -> None:
        self._event_bus.publish(QuitCommandEvent())
