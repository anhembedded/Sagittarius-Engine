"""
infrastructure/crypto_api.py
Real-time Binance WebSocket price stream manager using threads.

Usage example:
    manager = BinanceManager(symbol="ETHUSDT", timezone="Asia/Ho_Chi_Minh")
    manager.start()
"""

import logging
from datetime import datetime
from typing import Callable, Optional
from zoneinfo import ZoneInfo

from binance import ThreadedWebsocketManager

logger = logging.getLogger(__name__)

TickCallback = Callable[["TickerData"], None]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class TickerData:
    __slots__ = (
        "symbol", "last_price", "open_price", "high_price", "low_price",
        "price_change", "price_change_pct", "weighted_avg_price",
        "volume", "quote_volume", "best_bid", "best_ask",
        "trade_count", "event_time",
    )

    def __init__(self, raw: dict, timezone: ZoneInfo) -> None:
        self.symbol: str            = raw["s"]
        self.last_price: float      = float(raw["c"])
        self.open_price: float      = float(raw["o"])
        self.high_price: float       = float(raw["h"])
        self.low_price: float       = float(raw["l"])
        self.price_change: float    = float(raw["p"])
        self.price_change_pct: float = float(raw["P"])
        self.weighted_avg_price: float = float(raw["w"])
        self.volume: float          = float(raw["v"])
        self.quote_volume: float    = float(raw["q"])
        self.best_bid: float        = float(raw["b"])
        self.best_ask: float        = float(raw["a"])
        self.trade_count: int       = int(raw["n"])
        self.event_time: datetime   = datetime.fromtimestamp(
            raw["E"] / 1000.0, tz=timezone
        )

    def __repr__(self) -> str:
        ts = self.event_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        return (
            f"[{ts}] {self.symbol} | "
            f"Price: {self.last_price:.4f}  "
            f"Change: {self.price_change_pct:+.3f}%  "
            f"High: {self.high_price:.4f}  Low: {self.low_price:.4f}  "
            f"Vol: {self.volume:.2f}"
        )


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class BinanceManager:
    def __init__(
        self,
        symbol: str = "ETHUSDT",
        timezone: str = "UTC",
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        on_tick: Optional[TickCallback] = None,
    ) -> None:
        self.symbol:   str      = symbol.upper()
        self.timezone: ZoneInfo = ZoneInfo(timezone)
        self._api_key:    Optional[str] = api_key
        self._api_secret: Optional[str] = api_secret
        self._on_tick: Optional[TickCallback] = on_tick

        self._twm: Optional[ThreadedWebsocketManager] = None

    def start(self) -> None:
        self._twm = ThreadedWebsocketManager(
            api_key=self._api_key,
            api_secret=self._api_secret,
        )
        self._twm.start()

        logger.info(
            "BinanceManager started  symbol=%s  timezone=%s",
            self.symbol, self.timezone,
        )

        self._twm.start_symbol_ticker_socket(
            callback=self._handle_socket_message,
            symbol=self.symbol
        )

    def stop(self) -> None:
        if self._twm:
            self._twm.stop()
            self._twm = None
            logger.info("BinanceManager connection closed  symbol=%s", self.symbol)

    def _handle_socket_message(self, msg: dict) -> None:
        # Check for error message
        if msg.get('e') == 'error':
            logger.error(f"WebSocket error: {msg.get('m')}")
            return

        ticker = TickerData(msg, self.timezone)
        self._dispatch(ticker)

    def _dispatch(self, ticker: TickerData) -> None:
        if self._on_tick is None:
            print(ticker)
            return

        self._on_tick(ticker)

    def join(self) -> None:
        if self._twm:
            self._twm.join()
