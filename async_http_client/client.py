from dataclasses import dataclass, field
from typing import Dict, Any

import aiohttp
from aiohttp import ClientTimeout, ClientSession


@dataclass
class AsyncHTTPClient:
    __DEFAULT_SCHEME: str = field(default="http://", init=False)

    scheme: str
    host: str
    port: int = 80
    connect_timeout_sec: int = 1
    read_timeout_sec: int = 3
    concurrency: int = 10

    _session: ClientSession = field(default=None, init=False)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        if self._session is not None:
            return

        base_url = f'{self.__DEFAULT_SCHEME}{self.host}:{self.port}'
        timeout = ClientTimeout(
            sock_connect=self.connect_timeout_sec,
            sock_read=self.read_timeout_sec
        )
        connector = aiohttp.TCPConnector(
            limit_per_host=self.concurrency,
            force_close=True,
            enable_cleanup_closed=True
        )

        self._session = ClientSession(
            base_url=base_url,
            timeout=timeout,
            connector=connector
        )

    async def close(self):
        await self._session.close()


    async def request(
            self,
            method: str,
            url: str,
            **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to request
            **kwargs: Additional arguments to pass to aiohttp request
            
        Returns:
            Dict containing response data
        """
        if not self._session:
            await self.start()

        async with self._session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make a PATCH request."""
        return await self.request("PATCH", url, **kwargs)
