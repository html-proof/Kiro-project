import httpx
import logging
from fastapi import Response
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)

async def proxy_audio_stream(stream_url: str, range_header: str = None):
    headers = {}
    if range_header:
        headers["Range"] = range_header
    
    # We use a single request to avoid duplicate requests to YouTube
    # which can lead to throttling or 403 errors.
    
    async def stream_generator(response):
        try:
            async for chunk in response.aiter_bytes(chunk_size=8192):
                yield chunk
        except (httpx.ReadError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
            # Client disconnected or network error - this is normal for streaming
            logger.debug(f"Audio stream interrupted (normal): {type(e).__name__}")
        except Exception as e:
            logger.error(f"Unexpected audio streaming error: {e}")
        finally:
            await response.aclose()

    try:
        client = httpx.AsyncClient(timeout=60.0)
        # Using a context manager for the request but NOT for the stream itself
        # inside the generator to ensure the response remains open while yielding.
        request = client.build_request("GET", stream_url, headers=headers)
        response = await client.send(request, stream=True)
        
        # Forward relevant headers from the original response
        response_headers = {
            "Content-Type": response.headers.get("Content-Type", "audio/mpeg"),
            "Accept-Ranges": "bytes",
        }
        
        # Forward Content-Range if it exists (for partial content)
        if "Content-Range" in response.headers:
            response_headers["Content-Range"] = response.headers["Content-Range"]
            
        # IMPORTANT: We purposefully OMIT Content-Length here.
        # This prevents the "Response content shorter than Content-Length" RuntimeError
        # in uvicorn/starlette when a stream is interrupted.
        # FastAPI/Uvicorn will automatically use chunked transfer encoding.
        
        return StreamingResponse(
            stream_generator(response),
            status_code=response.status_code if response.status_code in [200, 206] else 200,
            headers=response_headers
        )
    except Exception as e:
        logger.error(f"Failed to initialize audio stream: {e}")
        return StreamingResponse(
            iter([]),
            status_code=500,
            media_type="audio/mpeg"
        )
