"""
crypto_api_show_case.py
======================
Demonstration of the BinanceManager module.

Run:
    python src/infrastructure/crypto_api/crypto_api.py
"""

import asyncio
import logging
import signal

from src.infrastructure.crypto_api import BinanceManager, TickerData

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("showcase")


async def demo_default(duration: float = 5.0) -> None:
    manager = BinanceManager(symbol="ETHUSDT", timezone="UTC")

    task = asyncio.create_task(manager.start())
    await asyncio.sleep(duration)
    await manager.stop()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


def my_sync_handler(ticker: TickerData) -> None:
    spread = ticker.best_ask - ticker.best_bid
    print(f"[SYNC] {ticker.symbol} Price={ticker.last_price:.4f} Spread={spread:.4f}")


async def demo_sync_callback(duration: float = 5.0) -> None:
    manager = BinanceManager(
        symbol="BTCUSDT",
        timezone="Asia/Ho_Chi_Minh",
        on_tick=my_sync_handler,
    )

    task = asyncio.create_task(manager.start())
    await asyncio.sleep(duration)
    await manager.stop()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


async def my_async_handler(ticker: TickerData) -> None:
    await asyncio.sleep(0)
    direction = "▲" if ticker.price_change >= 0 else "▼"
    print(f"[ASYNC] {ticker.symbol} {direction} {ticker.last_price:.4f}")


async def demo_async_callback(duration: float = 5.0) -> None:
    manager = BinanceManager(
        symbol="SOLUSDT",
        timezone="Asia/Ho_Chi_Minh",
        on_tick=my_async_handler,
    )

    task = asyncio.create_task(manager.start())
    await asyncio.sleep(duration)
    await manager.stop()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


async def demo_live(symbol: str = "ETHUSDT", timezone: str = "Asia/Ho_Chi_Minh") -> None:
    manager = BinanceManager(
        symbol=symbol,
        timezone=timezone,
        on_tick=my_async_handler,
    )

    loop = asyncio.get_running_loop()

    def _shutdown() -> None:
        logger.info("Shutdown signal received.")
        asyncio.ensure_future(manager.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _shutdown)
        except NotImplementedError:
            pass

    try:
        await manager.start()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass


async def main() -> None:
    await demo_default(duration=5)
    await demo_sync_callback(duration=5)
    await demo_async_callback(duration=5)
    await demo_live(symbol="ETHUSDT", timezone="Asia/Ho_Chi_Minh")


if __name__ == "__main__":
    asyncio.run(main())
