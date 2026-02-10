import httpx
from fastapi import Response
from fastapi.responses import StreamingResponse

async def proxy_audio_stream(stream_url: str, range_header: str = None):
    headers = {}
    if range_header:
        headers["Range"] = range_header
    
    async with httpx.AsyncClient() as client:
        response = await client.get(stream_url, headers=headers, timeout=30.0)
        
        return StreamingResponse(
            iter([response.content]),
            status_code=response.status_code,
            headers={
                "Content-Type": response.headers.get("Content-Type", "audio/mpeg"),
                "Content-Length": response.headers.get("Content-Length", ""),
                "Accept-Ranges": "bytes",
                "Content-Range": response.headers.get("Content-Range", "")
            }
        )
