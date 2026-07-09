from sagittarius_engine import App
from examples.trading_bot.app.exchanges.mock_exchange import MockExchange


class TradingStrategy:
    """
    @brief Simple mean reversion trading strategy.
    """

    def __init__(self, app: App, exchange: MockExchange) -> None:
        self.app = app
        self.exchange = exchange
        self.logger = app.context.logger

    def check_market(self) -> None:
        price = self.exchange.get_latest_price()
        self.logger.info(f"[Strategy] Checked price: {price:.2f}")

        if price < 99.0:
            self.logger.info(
                f"[Strategy] Price {price:.2f} is cheap! Spawning BUY order task..."
            )
            self.app.context.tasks.spawn(self.buy)
        elif price > 101.0:
            self.logger.info(
                f"[Strategy] Price {price:.2f} is high! Spawning SELL order task..."
            )
            self.app.context.tasks.spawn(self.sell)

    def buy(self) -> None:
        self.logger.info("[OrderExecution] Connecting to exchange to BUY...")
        order_id = self.exchange.place_order("BTCUSDT", "BUY", 0.01)
        self.logger.info(f"[OrderExecution] BUY Order completed: {order_id}")

    def sell(self) -> None:
        self.logger.info("[OrderExecution] Connecting to exchange to SELL...")
        order_id = self.exchange.place_order("BTCUSDT", "SELL", 0.01)
        self.logger.info(f"[OrderExecution] SELL Order completed: {order_id}")
