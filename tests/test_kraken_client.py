from time import time

import pytest

from kraken_client.client import KrakenClient


@pytest.fixture()
def kraken_client():
    yield KrakenClient()


class TestKrakenClient:
    test_ticker_pair = "ETHUSD"

    @pytest.mark.anyio
    async def test_assets_info(self, kraken_client):
        assert await kraken_client.get_assets_info(assets=["eth", "sol"])

    @pytest.mark.anyio
    async def test_tradable_pairs(self, kraken_client):
        assert await kraken_client.get_tradable_asset_pairs(["BTC/USD"])

    @pytest.mark.anyio
    async def test_get_ticker_info(self, kraken_client):
        assert await kraken_client.get_ticker_information(self.test_ticker_pair)

    @pytest.mark.anyio
    async def test_get_ohlc(self, kraken_client):
        assert await kraken_client.get_ohlc_data(self.test_ticker_pair, int(time() - 540))

    @pytest.mark.anyio
    async def test_get_order_book(self, kraken_client):
        assert await kraken_client.get_order_book(self.test_ticker_pair, count=20)

    @pytest.mark.anyio
    async def test_get_recent_trades(self, kraken_client):
        assert await kraken_client.get_recent_trades(self.test_ticker_pair, since=int(time() - 540), count=50)

    @pytest.mark.anyio
    async def test_get_recent_spread(self, kraken_client):
        assert await kraken_client.get_recent_spreads(self.test_ticker_pair, since=int(time() - 540))
