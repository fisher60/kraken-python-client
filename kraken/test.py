import asyncio

from kraken.client import KrakenClient

kraken_client = KrakenClient()


async def get_time_test():
    print(await kraken_client.get_server_time())


if __name__ == "__main__":
    asyncio.run(get_time_test())
