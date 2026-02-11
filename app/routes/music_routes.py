from fastapi import APIRouter, Query, Header, Request
from fastapi.responses import StreamingResponse
from app.services.youtube_search_service import search_youtube
from app.services.audio_resolver_service import resolve_audio_stream
from app.services.video_resolver_service import resolve_video_stream
from app.services.proxy_stream_service import proxy_audio_stream
from app.services.proxy_video_stream_service import proxy_video_stream
from app.utils.response_utils import success_response
from typing import Optional

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
    # Get the base URL from the request
    base_url = str(request.base_url).rstrip('/') if request else "http://localhost:8000"
    
    for result in results:
        if result.get('id'):
            # Construct the full stream URL that points to our play endpoint
            result['streamUrl'] = f"{base_url}/music/play?id={result['id']}&quality=saver"
    
    return success_response(results)

@router.get("/resolve")
async def resolve_audio(id: str = Query(...), quality: str = Query("saver")):
    result = await resolve_audio_stream(id, quality)
    if result:
        return success_response(result)
    return {"success": False, "message": "Failed to resolve"}

@router.get("/play")
@router.post("/play")
async def play_audio(
    request: Request,
    id: str = Query(None),
    quality: str = Query("saver"),
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
    
    if not id:
        return {"success": False, "message": "Missing id parameter"}
    
    stream_data = await resolve_audio_stream(id, quality)
    if stream_data:
        return await proxy_audio_stream(stream_data["stream_url"], range)
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
