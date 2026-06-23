from application.app_controller.AppController_api import IAppController
from application.event_bus.EventBus_api import EventBus
from application.app_events.app_events import (
    StartPriceCommandEvent, StopPriceCommandEvent, PriceUpdatedEvent, QuitCommandEvent
)
from application.logger.Logger_api import Logger

class AppControllerImpl(IAppController):
    """
    Coordinates Application Services (Use Cases) by listening to Domain Events.
    """
    def __init__(self, event_bus: EventBus, start_price_uc, stop_price_uc, logger: Logger):
        self._event_bus = event_bus
        self._start_price_uc = start_price_uc
        self._stop_price_uc = stop_price_uc
        self._logger = logger

    def start(self) -> None:
        self._event_bus.subscribe(StartPriceCommandEvent, self._handle_start_price)
        self._event_bus.subscribe(StopPriceCommandEvent, self._handle_stop_price)
        self._event_bus.subscribe(PriceUpdatedEvent, self._handle_price_updated)
        self._event_bus.subscribe(QuitCommandEvent, self._handle_quit)
        self._logger.info("AppControllerImpl started and listening to events.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(StartPriceCommandEvent, self._handle_start_price)
        self._event_bus.unsubscribe(StopPriceCommandEvent, self._handle_stop_price)
        self._event_bus.unsubscribe(PriceUpdatedEvent, self._handle_price_updated)
        self._event_bus.unsubscribe(QuitCommandEvent, self._handle_quit)
        self._logger.info("AppControllerImpl stopped.")

    def _handle_start_price(self, event: StartPriceCommandEvent) -> None:
        self._logger.debug(f"Received StartPriceCommandEvent for {event.symbol}")
        self._start_price_uc.execute(event.symbol)

    def _handle_stop_price(self, event: StopPriceCommandEvent) -> None:
        self._logger.debug(f"Received StopPriceCommandEvent for {event.symbol}")
        self._stop_price_uc.execute(event.symbol)

    def _handle_price_updated(self, event: PriceUpdatedEvent) -> None:
        # In a real UI, this might format data into a ViewModel and call a View presenter.
        # Here we just log it as the output.
        self._logger.info(f"[{event.symbol}] Price: {event.price:.4f} | Vol: {event.volume:.2f}")

    def _handle_quit(self, event: QuitCommandEvent) -> None:
        self._logger.info("Received QuitCommandEvent, initiating application shutdown...")
        # A broader shutdown sequence would go here, e.g., stopping all streams.
        self._stop_price_uc.execute("ETHUSDT")  # Example cleanup
