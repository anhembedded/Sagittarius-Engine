"""
crpto_api_show_case.py
======================
Demonstration of the BinanceManager module.

Three usage modes are shown:
    1. Default mode  – no callback, ticks are printed by the manager itself.
    2. Sync callback – a plain function receives each TickerData.
    3. Async callback – a coroutine receives each TickerData (most flexible).

Run:
    python src/infrastructure/crpto_api/crpto_api_show_case.py
"""

import asyncio
import logging
import signal

from src.infrastructure.crpto_api import BinanceManager, TickerData

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("showcase")


# ════════════════════════════════════════════════════════════════════════════
# Demo 1 – Default (no callback)
# The manager just prints each tick on its own.
# ════════════════════════════════════════════════════════════════════════════
async def demo_default(duration: float = 5.0) -> None:
    print("\n" + "═" * 60)
    print("  DEMO 1 – Default print mode (ETHUSDT, UTC)")
    print("═" * 60)

    manager = BinanceManager(symbol="ETHUSDT", timezone="UTC")

    task = asyncio.create_task(manager.start())
    await asyncio.sleep(duration)
    await manager.stop()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


# ════════════════════════════════════════════════════════════════════════════
# Demo 2 – Sync callback
# A plain function processes the tick; useful for simple pipelines.
# ════════════════════════════════════════════════════════════════════════════
def my_sync_handler(ticker: TickerData) -> None:
    spread = ticker.best_ask - ticker.best_bid
    print(
        f"[SYNC]  {ticker.event_time.strftime('%H:%M:%S %Z')}  "
        f"{ticker.symbol}  "
        f"Price={ticker.last_price:.4f}  "
        f"Spread={spread:.4f}  "
        f"Trades={ticker.trade_count:,}"
    )


async def demo_sync_callback(duration: float = 5.0) -> None:
    print("\n" + "═" * 60)
    print("  DEMO 2 – Sync callback  (BTCUSDT, Asia/Ho_Chi_Minh)")
    print("═" * 60)

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


# ════════════════════════════════════════════════════════════════════════════
# Demo 3 – Async callback
# A coroutine handles each tick; ideal for writing to DB, queues, etc.
# ════════════════════════════════════════════════════════════════════════════
async def my_async_handler(ticker: TickerData) -> None:
    # Simulate an async operation (e.g. writing to a database or queue)
    await asyncio.sleep(0)          # yield to event loop

    direction = "▲" if ticker.price_change >= 0 else "▼"
    print(
        f"[ASYNC] {ticker.event_time.strftime('%H:%M:%S %Z')}  "
        f"{ticker.symbol}  "
        f"{direction} {ticker.last_price:.4f}  "
        f"({ticker.price_change_pct:+.3f}%)  "
        f"H={ticker.high_price:.2f}  L={ticker.low_price:.2f}"
    )


async def demo_async_callback(duration: float = 5.0) -> None:
    print("\n" + "═" * 60)
    print("  DEMO 3 – Async callback  (SOLUSDT, Asia/Ho_Chi_Minh)")
    print("═" * 60)

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


# ════════════════════════════════════════════════════════════════════════════
# Demo 4 – Run indefinitely until Ctrl+C (production-style usage)
# ════════════════════════════════════════════════════════════════════════════
async def demo_live(symbol: str = "ETHUSDT", timezone: str = "Asia/Ho_Chi_Minh") -> None:
    print("\n" + "═" * 60)
    print(f"  DEMO 4 – Live stream  ({symbol}, {timezone})")
    print("  Press Ctrl+C to stop.")
    print("═" * 60)

    manager = BinanceManager(
        symbol=symbol,
        timezone=timezone,
        on_tick=my_async_handler,
    )

    loop = asyncio.get_running_loop()

    # Register Ctrl+C → graceful shutdown
    def _shutdown() -> None:
        logger.info("Shutdown signal received.")
        asyncio.ensure_future(manager.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _shutdown)
        except NotImplementedError:
            pass  # Windows does not support add_signal_handler for all signals

    try:
        await manager.start()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass

    print("\nStream stopped. Goodbye!")


# ════════════════════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════════════════════
async def main() -> None:
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          BinanceManager – Showcase                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Run the quick timed demos first
    await demo_default(duration=5)
    await demo_sync_callback(duration=5)
    await demo_async_callback(duration=5)

    # Then run live until the user hits Ctrl+C
    await demo_live(symbol="ETHUSDT", timezone="Asia/Ho_Chi_Minh")


if __name__ == "__main__":
    asyncio.run(main())
