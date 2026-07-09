import time
from sagittarius_engine import App
from examples.trading_bot.app.exchanges.mock_exchange import MockExchange
from examples.trading_bot.app.strategies.mean_reversion import TradingStrategy


def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Register logger extension module
    app.use(LoggerModule())

    # Create and register the hosted exchange connection
    exchange = MockExchange()
    app.context.hosted_services.register(exchange)

    # Boot the application
    app.boot()

    # Create strategy
    strategy = TradingStrategy(app, exchange)

    # Schedule strategy checks every 0.1 seconds
    app.context.scheduler.every(seconds=0.1).do(strategy.check_market)

    # Let the trading bot execute for 0.5 seconds
    time.sleep(0.5)

    # Shutdown gracefully
    app.stop()


if __name__ == "__main__":
    main()
