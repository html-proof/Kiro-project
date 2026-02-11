from fastapi import APIRouter, Query, Header, Request
from fastapi.responses import StreamingResponse
from app.services.youtube_search_service import search_youtube
from app.services.audio_resolver_service import resolve_audio_stream
from app.services.video_resolver_service import resolve_video_stream
from app.services.proxy_stream_service import proxy_audio_stream
from app.services.proxy_video_stream_service import proxy_video_stream
from app.utils.response_utils import success_response
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search")
async def search_music(
    q: str = Query(...),
    user_id: Optional[str] = Query(None),
    request: Request = None
):
    """
    Search for songs with intelligent filtering and personalization.
    
    - Filters out non-music content (trailers, movies, news, etc.)
    - Blocks spam music types (8D, slowed+reverb, etc.)
    - Prioritizes official channels and trusted labels
    - Personalizes results based on user's liked artists
    """
    results = await search_youtube(q, limit=10, user_id=user_id)
    
    # Add streamUrl to each result for direct playback
    # Get the base URL from the request, with fallback
    if request:
        # Try to get the base URL from headers first (for proxied requests)
        forwarded_proto = request.headers.get('x-forwarded-proto', 'http')
        forwarded_host = request.headers.get('x-forwarded-host')
        
        if forwarded_host:
            base_url = f"{forwarded_proto}://{forwarded_host}"
        else:
            base_url = str(request.base_url).rstrip('/')
    else:
        base_url = "http://localhost:8000"
    
    logger.info(f"Search request base_url: {base_url}")
    logger.info(f"Request headers: {dict(request.headers) if request else 'No request'}")
    
    for result in results:
        if result.get('id'):
            # Construct the full stream URL that points to our play endpoint
            # Use 'high' quality by default for better audio experience
            result['streamUrl'] = f"{base_url}/music/play?id={result['id']}&quality=high"
            logger.info(f"Generated streamUrl for {result.get('title')}: {result['streamUrl']}")
    
    logger.info(f"Returning {len(results)} results")
    return success_response(results)

@router.get("/resolve")
async def resolve_audio(id: str = Query(...), quality: str = Query("high")):
    result = await resolve_audio_stream(id, quality)
    if result:
        return success_response(result)
    return {"success": False, "message": "Failed to resolve"}

@router.get("/play")
@router.post("/play")
async def play_audio(
    request: Request,
    id: str = Query(None),
    quality: str = Query("high"),
    range: Optional[str] = Header(None)
):
    # For POST requests, try to get id from query params or body
    if not id:
        try:
            body = await request.json()
            id = body.get('id') or body.get('video_id')
            quality = body.get('quality', quality)
        except:
            # Try form data
            try:
                form = await request.form()
                id = form.get('id') or form.get('video_id')
                quality = form.get('quality', quality)
            except:
                pass
    
    logger.info(f"Play request - id: {id}, quality: {quality}, method: {request.method}")
    
    if not id:
        logger.error("Play request missing id parameter")
        return {"success": False, "message": "Missing id parameter"}
    
    stream_data = await resolve_audio_stream(id, quality)
    if stream_data:
        logger.info(f"Streaming audio for id: {id}")
        return await proxy_audio_stream(stream_data["stream_url"], range)
    
    logger.error(f"Failed to resolve stream for id: {id}")
    return {"success": False, "message": "Failed to stream"}

@router.get("/preview")
async def preview_audio(id: str = Query(...), range: Optional[str] = Header(None)):
    stream_data = await resolve_audio_stream(id, "ultra")
    if stream_data:
        return await proxy_audio_stream(stream_data["stream_url"], range)
    return {"success": False, "message": "Failed to preview"}

@router.get("/resolve-video")
async def resolve_video(id: str = Query(...), quality: str = Query("low")):
    result = await resolve_video_stream(id, quality)
    if result:
        return success_response(result)
    return {"success": False, "message": "Failed to resolve video"}

@router.get("/play-video")
async def play_video(
    id: str = Query(...),
    quality: str = Query("low"),
    range: Optional[str] = Header(None)
):
    stream_data = await resolve_video_stream(id, quality)
    if stream_data:
        return await proxy_video_stream(stream_data["stream_url"], range)
    return {"success": False, "message": "Failed to stream video"}
