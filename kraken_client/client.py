from httpx import AsyncClient, RequestError

from kraken_client.models import TradeableAssetPairsInfo


class KrakenClient:
    def __init__(
            self,
            base_api_url: str = "https://api.kraken.com/0"
    ):
        self.base_api_url = base_api_url
        self.private_api_url = f"{base_api_url}/private"
        self.public_api_url = f"{base_api_url}/public"

    async def _get_public(self, resource_path: str, key: str | None = None, params: dict | None = None):
        async with AsyncClient() as client:
            resp = (await client.get(f"{self.public_api_url}/{resource_path}", params=params)).json()

        if errors := resp.get("error"):
            raise RequestError(errors)

        result = resp["result"]

        if key is not None:
            try:
                return result.get(key)
            except KeyError:
                raise KeyError(f"Key '{key}' not in response result")
        else:
            return result

    async def get_server_time(self):
        return await self._get_public("Time", "unixtime")

    async def get_system_status(self):
        return await self._get_public("SystemStatus", "status")

    async def get_assets_info(self, assets: list[str] | None = None, aclass: str = "currency"):
        params = {
            "aclass": aclass
        }

        if assets is not None:
            params["asset"] = ",".join([x.upper() for x in assets])

        return await self._get_public("Assets", params=params)

    async def get_tradable_asset_pairs(
            self,
            pairs: list[str],
            info: TradeableAssetPairsInfo = TradeableAssetPairsInfo.info
    ):
        """Each pair is a ticker_pair

        Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        params = {
            "ticker_pair": ",".join(pairs),
            "info": info
        }
        return await self._get_public("AssetPairs", params=params)

    async def get_ticker_information(self, ticker_pair: str | None):
        """Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        if ticker_pair:
            params = {
                "pair": ticker_pair
            }
        else:
            params = None

        return await self._get_public("Ticker", params=params)

    async def get_ohlc_data(self, ticker_pair: str, since: int, minute_interval: int = 1):
        """Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        params = {
            "pair": ticker_pair,
            "interval": minute_interval,
            "since": since
        }

        return await self._get_public("OHLC", params=params)

    async def get_order_book(self, ticker_pair: str, count: int = 100):
        """Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        params = {
            "pair": ticker_pair,
            "count": count
        }

        return await self._get_public("Depth", params=params)

    async def get_recent_trades(self, ticker_pair: str, since: int, count: int = 100):
        """Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        params = {
            "pair": ticker_pair,
            "since": since,
            "count": count
        }

        return await self._get_public("Trades", params=params)

    async def get_recent_spreads(self, ticker_pair: str, since: int):
        """Ticker pair is a valid combination of asset codes as outlined in kraken support

        https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
        """
        params = {
            "pair": ticker_pair,
            "since": since
        }

        return await self._get_public("Spread", params=params)
