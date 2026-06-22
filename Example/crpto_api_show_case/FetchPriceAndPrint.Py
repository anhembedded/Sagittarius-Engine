import asyncio
from binance import AsyncClient, BinanceSocketManager



async def main():
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)
    async with bsm.symbol_ticker_socket(symbol='ETHUSDT') as stream:
        while True:
            msg = await stream.recv()
            print(f"{msg}")

if __name__ == "__main__":