# Async HTTP Client

A simple and efficient async HTTP client built with Python's asyncio and aiohttp.

## Features

- Async HTTP client with support for all major HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Context manager support for easy resource management
- Configurable timeouts and headers
- SSL verification control
- Base URL support for API clients

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
import asyncio
from async_http_client.client import AsyncHTTPClient

async def main():
    async with AsyncHTTPClient(
        base_url="https://api.example.com",
        headers={"Content-Type": "application/json"}
    ) as client:
        # GET request
        response = await client.get("/endpoint")
        print(response)

        # POST request
        data = {"key": "value"}
        response = await client.post("/endpoint", json=data)
        print(response)

asyncio.run(main())
```

### Manual Session Management

```python
import asyncio
from async_http_client.client import AsyncHTTPClient

async def main():
    client = AsyncHTTPClient(base_url="https://api.example.com")
    try:
        await client.start()
        response = await client.get("/endpoint")
        print(response)
    finally:
        await client.close()

asyncio.run(main())
```

## API Reference

### AsyncHTTPClient

#### Initialization

```python
client = AsyncHTTPClient(
    base_url: Optional[str] = None,
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True
)
```

#### Methods

- `get(url: str, **kwargs) -> Dict[str, Any]`
- `post(url: str, **kwargs) -> Dict[str, Any]`
- `put(url: str, **kwargs) -> Dict[str, Any]`
- `delete(url: str, **kwargs) -> Dict[str, Any]`
- `patch(url: str, **kwargs) -> Dict[str, Any]`
- `request(method: str, url: str, **kwargs) -> Dict[str, Any]`

## License

MIT 