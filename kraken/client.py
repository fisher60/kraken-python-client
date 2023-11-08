from httpx import AsyncClient, RequestError


class KrakenClient:
    def __init__(
            self,
            base_api_url: str = "https://api.kraken.com/0"
    ):
        self.base_api_url = base_api_url
        self.private_api_url = f"{base_api_url}/private"
        self.public_api_url = f"{base_api_url}/public"

    async def _get_public(self, resource_path):
        async with AsyncClient() as client:
            data = (await client.get(f"{self.public_api_url}/{resource_path}")).json()

        if errors := data.get("error"):
            raise RequestError(errors)

        return data

    async def get_server_time(self):
        return (await self._get_public("Time")).get("unixtime")
