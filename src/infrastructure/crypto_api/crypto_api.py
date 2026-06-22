"""
infrastructure/crypto_api.py
Real-time Binance WebSocket price stream manager.

Usage example:
    manager = BinanceManager(symbol="ETHUSDT", timezone="Asia/Ho_Chi_Minh")
    asyncio.run(manager.start())
"""

import asyncio
import logging
from datetime import datetime
from typing import Awaitable, Callable, Optional, Union
from zoneinfo import ZoneInfo

from binance import AsyncClient, BinanceSocketManager

logger = logging.getLogger(__name__)

# Type alias: callback can be sync or async
TickCallback = Union[
    Callable[["TickerData"], None],
    Callable[["TickerData"], Awaitable[None]],
]


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
        self.high_price: float      = float(raw["h"])
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

        self._client:  Optional[AsyncClient] = None
        self._running: bool = False

    async def start(self) -> None:
        self._client  = await AsyncClient.create(
            api_key=self._api_key,
            api_secret=self._api_secret,
        )
        bsm = BinanceSocketManager(self._client)
        self._running = True

        logger.info(
            "BinanceManager started  symbol=%s  timezone=%s",
            self.symbol, self.timezone,
        )

        try:
            async with bsm.symbol_ticker_socket(symbol=self.symbol) as stream:
                while self._running:
                    raw = await stream.recv()
                    ticker = TickerData(raw, self.timezone)
                    await self._dispatch(ticker)
        except asyncio.CancelledError:
            logger.info("BinanceManager stream cancelled.")
        finally:
            await self._close()

    async def stop(self) -> None:
        self._running = False

    async def _dispatch(self, ticker: TickerData) -> None:
        if self._on_tick is None:
            print(ticker)
            return

        if asyncio.iscoroutinefunction(self._on_tick):
            await self._on_tick(ticker)
        else:
            self._on_tick(ticker)

    async def _close(self) -> None:
        if self._client is not None:
            await self._client.close_connection()
            self._client = None
            logger.info("BinanceManager connection closed  symbol=%s", self.symbol)
