import asyncio
from binance import AsyncClient, BinanceSocketManager


async def main():
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)
    streams = ["btcusdt@kline_1m", "ethusdt@kline_1m"]
    socket = bsm.multiplex_socket(streams)
    print("Connecting...")
    async with socket as tscm:
        print("Connected. Waiting for 3 ticks...")
        for i in range(3):
            res = await tscm.recv()
            print(f"Tick {i}: {res}")
    await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())
