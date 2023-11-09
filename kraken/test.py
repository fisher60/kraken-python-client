import asyncio
from time import time

from kraken.client import KrakenClient

kraken_client = KrakenClient()

to_test = [
    kraken_client.get_server_time,
    kraken_client.get_assets_info,
    kraken_client.get_system_status
]


async def test_assets_info():
    print(await kraken_client.get_assets_info(assets=["eth", "sol"]))


async def test_tradable_pairs():
    print(await kraken_client.get_tradable_asset_pairs(["BTC/USD"]))


async def test_get_ticker_info():
    print(await kraken_client.get_ticker_information("ETHUSD"))


async def test_get_ohlc():
    print(await kraken_client.get_ohlc_data("ETHUSD", int(time() - 540)))


async def test_get_order_book():
    print(await kraken_client.get_order_book("ETHUSD", count=20))


async def test_get_recent_trades():
    print(await kraken_client.get_recent_trades("ETHUSD", since=int(time() - 540), count=50))


async def test_get_recent_spread():
    print(await kraken_client.get_recent_spreads("ETHUSD", since=int(time() - 540)))


async def test_all():
    for func in to_test:
        print(await func())


if __name__ == "__main__":
    asyncio.run(test_get_recent_spread())
