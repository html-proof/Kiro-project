"""
User Profile Routes - Comprehensive user data tracking and management
"""
from fastapi import APIRouter, Query, Body
from typing import List, Optional
from app.services.user_profile_service import get_user_profile_service
from app.utils.response_utils import success_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
profile_service = get_user_profile_service()

# ==================== USER PREFERENCES ====================

@router.post("/preferences")
async def set_preferences(
    user_id: str = Query(...),
    languages: List[str] = Body(...),
    moods: List[str] = Body(...)
):
    """
    Set user preferences (asked once on first login)
    
    Example:
    POST /profile/preferences?user_id=USER123
    {
        "languages": ["English", "Hindi", "Tamil"],
        "moods": ["Happy", "Energetic", "Chill", "Romantic"]
    }
    """
    success = await profile_service.set_user_preferences(user_id, languages, moods)
    if success:
        return success_response({"message": "Preferences saved successfully"})
    return {"success": False, "message": "Failed to save preferences"}

@router.get("/preferences")
async def get_preferences(user_id: str = Query(...)):
    """Get user's saved preferences"""
    prefs = await profile_service.get_user_preferences(user_id)
    if prefs:
        return success_response(prefs)
    return {"success": False, "message": "No preferences found"}

# ==================== SEARCH TRACKING ====================

@router.post("/track/search")
async def track_search(
    user_id: str = Query(...),
    query: str = Body(...),
    results_count: int = Body(...)
):
    """
    Track user's search query
    
    Example:
    POST /profile/track/search?user_id=USER123
    {
        "query": "romantic songs",
        "results_count": 10
    }
    """
    success = await profile_service.track_search(user_id, query, results_count)
    if success:
        return success_response({"message": "Search tracked"})
    return {"success": False, "message": "Failed to track search"}

@router.get("/search-history")
async def get_search_history(
    user_id: str = Query(...),
    limit: int = Query(50)
):
    """Get user's search history"""
    history = await profile_service.get_search_history(user_id, limit)
    return success_response(history)

# ==================== PLAY TRACKING ====================

@router.post("/track/play")
async def track_play(
    user_id: str = Query(...),
    song_data: dict = Body(...)
):
    """
    Track when user plays a song
    
    Example:
    POST /profile/track/play?user_id=USER123
    {
        "id": "VIDEO_ID",
        "title": "Song Title",
        "artist": "Artist Name",
        "duration": 180,
        "thumbnail": "https://..."
    }
    """
    success = await profile_service.track_play(user_id, song_data)
    if success:
        return success_response({"message": "Play tracked"})
    return {"success": False, "message": "Failed to track play"}

@router.get("/play-history")
async def get_play_history(
    user_id: str = Query(...),
    limit: int = Query(100)
):
    """Get user's play history"""
    history = await profile_service.get_play_history(user_id, limit)
    return success_response(history)

# ==================== PLAYBACK POSITION (RESUME) ====================

@router.post("/playback/position")
async def save_position(
    user_id: str = Query(...),
    song_id: str = Body(...),
    position_ms: int = Body(...),
    duration_ms: int = Body(...)
):
    """
    Save playback position for resume
    
    Example:
    POST /profile/playback/position?user_id=USER123
    {
        "song_id": "VIDEO_ID",
        "position_ms": 45000,
        "duration_ms": 180000
    }
    """
    success = await profile_service.save_playback_position(user_id, song_id, position_ms, duration_ms)
    if success:
        return success_response({"message": "Position saved"})
    return {"success": False, "message": "Failed to save position"}

@router.get("/playback/position")
async def get_position(
    user_id: str = Query(...),
    song_id: str = Query(...)
):
    """Get saved playback position for resume"""
    position = await profile_service.get_playback_position(user_id, song_id)
    if position:
        return success_response(position)
    return {"success": False, "message": "No saved position"}

@router.delete("/playback/position")
async def clear_position(
    user_id: str = Query(...),
    song_id: str = Query(...)
):
    """Clear playback position (when song completed)"""
    success = await profile_service.clear_playback_position(user_id, song_id)
    if success:
        return success_response({"message": "Position cleared"})
    return {"success": False, "message": "Failed to clear position"}

# ==================== OFFLINE DOWNLOADS ====================

@router.post("/offline/add")
async def add_offline_song(
    user_id: str = Query(...),
    song_data: dict = Body(...),
    file_path: str = Body(...),
    file_size: int = Body(...)
):
    """
    Track offline downloaded song
    
    Example:
    POST /profile/offline/add?user_id=USER123
    {
        "song_data": {
            "id": "VIDEO_ID",
            "title": "Song Title",
            "artist": "Artist Name",
            "duration": 180,
            "thumbnail": "https://...",
            "quality": "ultra"
        },
        "file_path": "/storage/music/song.mp3",
        "file_size": 1048576
    }
    """
    success = await profile_service.track_offline_download(user_id, song_data, file_path, file_size)
    if success:
        return success_response({"message": "Offline song tracked"})
    return {"success": False, "message": "Failed to track offline song"}

@router.get("/offline/list")
async def get_offline_songs(user_id: str = Query(...)):
    """Get list of offline downloaded songs"""
    songs = await profile_service.get_offline_songs(user_id)
    return success_response(songs)

@router.delete("/offline/remove")
async def remove_offline_song(
    user_id: str = Query(...),
    song_id: str = Query(...)
):
    """Remove song from offline list"""
    success = await profile_service.remove_offline_song(user_id, song_id)
    if success:
        return success_response({"message": "Offline song removed"})
    return {"success": False, "message": "Failed to remove offline song"}

# ==================== USER STATISTICS ====================

@router.get("/stats")
async def get_user_stats(user_id: str = Query(...)):
    """
    Get comprehensive user statistics
    
    Returns:
    - Preferences (languages, moods)
    - Play statistics
    - Top played songs
    - Recent searches
    - Offline songs count
    """
    stats = await profile_service.get_user_stats(user_id)
    return success_response(stats)

@router.get("/recommendation-data")
async def get_recommendation_data(user_id: str = Query(...)):
    """
    Get all data needed for personalized recommendations
    
    Used by recommendation engine to generate unique recommendations per user
    """
    data = await profile_service.get_recommendation_data(user_id)
    return success_response(data)
