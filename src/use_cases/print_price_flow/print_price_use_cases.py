from src.domain.crypto_stream.crypto_stream_port import CryptoStreamPort, Ticker
from application.logger.Logger_api import Logger
from application.event_bus.EventBus_api import EventBus
from application.app_events.app_events import PriceUpdatedEvent

class StartPrintPriceUseCase:
    def __init__(self, crypto_stream: CryptoStreamPort, logger: Logger, event_bus: EventBus):
        self._crypto_stream = crypto_stream
        self._logger = logger
        self._event_bus = event_bus

    def execute(self, symbol: str) -> None:
        self._logger.info(f"Starting price stream for {symbol}...")

        def on_tick(ticker: Ticker) -> None:
            # Emit a domain event instead of logging directly (Controller/UI will handle log/display)
            event = PriceUpdatedEvent(symbol=ticker.symbol, price=ticker.price, volume=ticker.volume)
            self._event_bus.publish(event)

        self._crypto_stream.start_stream(symbol, on_tick)


class StopPrintPriceUseCase:
    def __init__(self, crypto_stream: CryptoStreamPort, logger: Logger):
        self._crypto_stream = crypto_stream
        self._logger = logger

    def execute(self, symbol: str) -> None:
        self._logger.info(f"Stopping price stream for {symbol}...")
        self._crypto_stream.stop_stream(symbol)
