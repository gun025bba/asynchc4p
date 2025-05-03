import asyncio
from async_http_client.client import AsyncHTTPClient

async def main():
    # Example 1: Using context manager
    async with AsyncHTTPClient(
        base_url="https://jsonplaceholder.typicode.com",
        headers={"Content-Type": "application/json"}
    ) as client:
        # GET request
        todos = await client.get("/todos/1")
        print("GET Response:", todos)

        # POST request
        new_todo = {
            "title": "New Todo",
            "completed": False,
            "userId": 1
        }
        created_todo = await client.post("/todos", json=new_todo)
        print("POST Response:", created_todo)
    AsyncHTTPClient()

    # Example 2: Manual session management
    client = AsyncHTTPClient(
        base_url="https://jsonplaceholder.typicode.com"
    )
    try:
        await client.start()
        # PUT request
        updated_todo = {
            "title": "Updated Todo",
            "completed": True,
            "userId": 1
        }
        result = await client.put("/todos/1", json=updated_todo)
        print("PUT Response:", result)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 