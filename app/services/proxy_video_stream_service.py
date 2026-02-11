import httpx
import logging
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)

async def proxy_video_stream(stream_url: str, range_header: str = None):
    headers = {}
    if range_header:
        headers["Range"] = range_header
    
    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("GET", stream_url, headers=headers) as response:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        yield chunk
        except (httpx.ReadError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
            # Client disconnected or network error - this is normal for streaming
            logger.debug(f"Video stream interrupted (normal): {type(e).__name__}")
        except Exception as e:
            logger.error(f"Unexpected video streaming error: {e}")
    
    # Get initial response to extract headers
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.head(stream_url, headers=headers)
            
            return StreamingResponse(
                stream_generator(),
                status_code=response.status_code if response.status_code in [200, 206] else 200,
                headers={
                    "Content-Type": response.headers.get("Content-Type", "video/mp4"),
                    "Accept-Ranges": "bytes",
                    "Content-Length": response.headers.get("Content-Length", ""),
                    "Content-Range": response.headers.get("Content-Range", "")
                }
            )
    except Exception as e:
        logger.error(f"Failed to initialize video stream: {e}")
        # Fallback: return stream without pre-fetching headers
        return StreamingResponse(
            stream_generator(),
            media_type="video/mp4",
            headers={"Accept-Ranges": "bytes"}
        )
