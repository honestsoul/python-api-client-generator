# api_client_generator/async_support/async_client.py

import aiohttp
from typing import Dict, Any
from ..utils.rate_limiter import RateLimiter
from ..authentication.auth_handler import AuthHandler

class AsyncAPIClient:
    def __init__(self, base_url: str, auth_handler: AuthHandler):
        self.base_url = base_url
        self.auth_handler = auth_handler
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    @RateLimiter(calls=100, period=60)  # Adjust as needed
    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        auth = self.auth_handler.get_auth('default')  # Adjust based on your auth setup
        headers = kwargs.pop('headers', {})
        headers.update(auth.get_headers())

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request('GET', endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request('POST', endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request('PUT', endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request('DELETE', endpoint, **kwargs)

# Usage:
# async with AsyncAPIClient(base_url, auth_handler) as client:
#     data = await client.get('/endpoint')