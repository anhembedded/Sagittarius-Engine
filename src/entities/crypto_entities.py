from dataclasses import dataclass
from typing import Optional



class PriceBuffer:
    def __init__(self, data: list[float]):
        self._price_on_second: list[float] = data
        self._unit: str = "USDT"

    def get_price(self):
        return self._price_on_second

    def update_price(self, price: float):
        self._price_on_second.append(price)
        if len(self._price_on_second) > getattr(self, "_length", 0):
            self._price_on_second.pop(0)


class Crypto:
    def __init__(self, name: str, symbol: str, price_buffer: PriceBuffer):
        self._name = name
        self._symbol = symbol
        self._price_buffer: PriceBuffer = price_buffer

    def __str__(self):
        return f"{self._symbol}: {self._price_buffer.get_price()}"

    def get_price(self):
        return self._price_buffer.get_price()

    def update_price(self, price: float):
        self._price_buffer.update_price(price)
