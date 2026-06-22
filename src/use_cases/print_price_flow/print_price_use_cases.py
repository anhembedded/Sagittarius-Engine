from src.domain.crypto_stream.crypto_stream_port import CryptoStreamPort, Ticker
from src.domain.logger.Logger_api import Logger

class StartPrintPriceUseCase:
    def __init__(self, crypto_stream: CryptoStreamPort, logger: Logger):
        self._crypto_stream = crypto_stream
        self._logger = logger

    def execute(self, symbol: str) -> None:
        self._logger.info(f"Starting price stream for {symbol}...")

        def on_tick(ticker: Ticker) -> None:
            self._logger.info(f"[{ticker.symbol}] Price: {ticker.price:.4f} | Vol: {ticker.volume:.2f}")

        self._crypto_stream.start_stream(symbol, on_tick)


class StopPrintPriceUseCase:
    def __init__(self, crypto_stream: CryptoStreamPort, logger: Logger):
        self._crypto_stream = crypto_stream
        self._logger = logger

    def execute(self, symbol: str) -> None:
        self._logger.info(f"Stopping price stream for {symbol}...")
        self._crypto_stream.stop_stream(symbol)
