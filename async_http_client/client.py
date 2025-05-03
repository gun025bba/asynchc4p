import asyncio
import aiohttp
from typing import Optional, Dict, Any, Union
from aiohttp import ClientTimeout, ClientSession


class AsyncHTTPClient:
    __DEFAULT_SCHEME = "http://"
    
    def __init__(
            self,
            scheme: str,
            host: str,
            port: int = 80,
            connect_timeout_sec=1,
            read_timeout_sec=3,
            concurrency=10,
            headers: Optional[Dict[str, str]] = None,
            verify_ssl: bool = True
    ):
        """
        Initialize the async HTTP client.
        
        Args:
            base_url: Base URL for all requests
            timeout: Default timeout in seconds
            headers: Default headers for all requests
            verify_ssl: Whether to verify SSL certificates
        """
        base_url = f'{self.__DEFAULT_SCHEME}{host}:{port}'

        client_timeout = ClientTimeout(
            sock_connect=connect_timeout_sec,
            sock_read=read_timeout_sec
        )
        connector = aiohttp.TCPConnector(
            limit_per_host=concurrency,
            force_close=False
        )

        client_session = ClientSession(
            base_url=base_url,
            timeout=client_timeout,

        )

        self.base_url = base_url
        self.timeout = ClientTimeout(total=timeout)
        self.headers = headers or {}
        self.verify_ssl = verify_ssl
        self._session: Optional[ClientSession] = None

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        """Start the client session."""
        if self._session is None:
            self._session = ClientSession(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.headers,
                connector=aiohttp.TCPConnector(verify_ssl=self.verify_ssl)
            )

    async def close(self):
        """Close the client session."""
        if self._session:
            await self._session.close()
            self._session = None

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
