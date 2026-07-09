import time
import random
from sagittarius_engine.runtime import IHostedService


class MockExchange(IHostedService):
    """
    @brief Simulates a crypto exchange connection.
    """

    def __init__(self) -> None:
        self.price = 100.0
        self.started = False

    def start(self, context) -> None:
        self.started = True
        context.logger.info("MockExchange connected. Price stream ready.")

    def stop(self, context) -> None:
        self.started = False
        context.logger.info("MockExchange disconnected.")

    def get_latest_price(self) -> float:
        self.price += random.uniform(-1.0, 1.0)
        return self.price

    def place_order(self, symbol: str, side: str, amount: float) -> str:
        time.sleep(0.05)
        return f"ORDER_ID_{random.randint(1000, 9999)}"
