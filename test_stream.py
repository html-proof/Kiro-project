
import asyncio
import httpx

async def test_stream_headers():
    url = "http://localhost:8000/play?id=dQw4w9WgXcQ"
    print(f"Testing headers for {url}...")
    try:
        async with httpx.AsyncClient() as client:
            # We only need the headers, so we use a GET with stream=True and then close
            async with client.stream("GET", url) as response:
                print(f"Status: {response.status_code}")
                print("Headers:")
                for name, value in response.headers.items():
                    print(f"  {name}: {value}")
                
                if "Content-Length" in response.headers:
                    print("❌ FAILED: Content-Length header is present!")
                else:
                    print("✅ SUCCESS: Content-Length header is absent.")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the backend is running (python start.py)")

if __name__ == "__main__":
    asyncio.run(test_stream_headers())
