from dataclasses import dataclass
from typing import Optional



class PriceBuffer:
    def __init__(self, data : list[float]):
        self._price_on_second : list[float] = data
        self._unit : str = "USDT"

    def getPrice(self):
        return self._price_on_second

    def updatePrice(self, price : float):
        self._price_on_second.append(price)
        if len(self._price_on_second) > self._lenght:
            self._price_on_second.pop(0)
    

class Crypto:
    def __init__(self, name : str , symbol : str , priceBuffer : PriceBuffer):
        self._name = name
        self._symbol = symbol
        self._priceBuffer : PriceBuffer = priceBuffer

    def __str__(self):
        return f"{self.symbol}: {self.priceBuffer.getPrice()}"

    def getPrice(self):
        return self._priceBuffer.getPrice()
    
    def updatePrice(self, price : float):
        self._priceBuffer.updatePrice(price)