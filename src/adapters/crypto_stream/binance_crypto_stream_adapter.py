import threading
from typing import Dict

from src.domain.crypto_stream.crypto_stream_port import CryptoStreamPort, Ticker, TickCallback
from src.infrastructure.crypto_api.crypto_api import BinanceManager, TickerData

class BinanceCryptoStreamAdapter(CryptoStreamPort):
    def __init__(self) -> None:
        self._managers: Dict[str, BinanceManager] = {}
        self._lock = threading.Lock()

    def start_stream(self, symbol: str, on_tick: TickCallback) -> None:
        with self._lock:
            if symbol in self._managers:
                return  # Already running

            # Define a closure that translates TickerData to Domain Ticker
            def handle_tick(ticker_data: TickerData) -> None:
                domain_ticker = Ticker(
                    symbol=ticker_data.symbol,
                    price=ticker_data.last_price,
                    volume=ticker_data.volume
                )
                on_tick(domain_ticker)

            manager = BinanceManager(
                symbol=symbol,
                timezone="UTC",
                on_tick=handle_tick
            )
            manager.start()
            self._managers[symbol] = manager

    def stop_stream(self, symbol: str) -> None:
        with self._lock:
            manager = self._managers.get(symbol)
            if manager:
                manager.stop()
                manager.join()
                del self._managers[symbol]
