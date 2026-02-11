from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.firebase.firebase_auth import verify_token
from app.firestore.firestore_collections import get_user_ref
from app.services.user_history_service import add_to_history, get_user_history, update_progress
from app.services.user_like_service import add_like, get_user_likes, remove_like
# Temporarily disabled due to import issue
# from app.services.recommendation_service import get_user_recommendations
from app.utils.response_utils import success_response

router = APIRouter()

class PreferencesRequest(BaseModel):
    selected_languages: list
    selected_artists: list

class PlayRequest(BaseModel):
    video_id: str
    title: str = ""
    artist: str = ""
    thumbnail: str = ""
    duration: int = 0
    language: str = ""

class LikeRequest(BaseModel):
    video_id: str
    title: str = ""
    artist: str = ""
    thumbnail: str = ""
    duration: int = 0
    language: str = ""

class ProgressRequest(BaseModel):
    video_id: str
    position: int = 0
    duration: int = 0

@router.post("/preferences")
async def save_preferences(request: PreferencesRequest, token: dict = Depends(verify_token)):
    uid = token["uid"]
    user_ref = get_user_ref(uid)
    user_ref.update({
        "selected_languages": request.selected_languages,
        "selected_artists": request.selected_artists
    })
    return success_response({}, "Preferences saved")

@router.post("/play")
async def track_play(request: PlayRequest, token: dict = Depends(verify_token)):
    try:
        uid = token["uid"]
        await add_to_history(uid, request.dict())
        return success_response({}, "Play tracked")
    except Exception as e:
        print(f"Error tracking play: {e}")
        return success_response({}, "Play tracking failed but continuing")

@router.post("/like")
async def like_song(request: LikeRequest, token: dict = Depends(verify_token)):
    uid = token["uid"]
    await add_like(uid, request.dict())
    return success_response({}, "Song liked")

@router.post("/progress")
async def save_progress(request: ProgressRequest, token: dict = Depends(verify_token)):
    try:
        uid = token["uid"]
        await update_progress(uid, request.video_id, request.position, request.duration)
        return success_response({}, "Progress saved")
    except Exception as e:
        print(f"Error saving progress: {e}")
        return success_response({}, "Progress save failed but continuing")

@router.get("/history")
async def get_history(token: dict = Depends(verify_token)):
    uid = token["uid"]
    history = await get_user_history(uid)
    return success_response(history)

@router.get("/likes")
async def get_likes(token: dict = Depends(verify_token)):
    uid = token["uid"]
    likes = await get_user_likes(uid)
    return success_response(likes)

@router.get("/recent")
async def get_recent(token: dict = Depends(verify_token)):
    uid = token["uid"]
    history = await get_user_history(uid, limit=20)
    return success_response(history)

@router.get("/recommend")
async def get_recommendations(token: dict = Depends(verify_token)):
    """Temporarily disabled - recommendation service being fixed"""
    return success_response([], "Recommendations temporarily unavailable")
