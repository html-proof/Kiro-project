from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.firebase.firebase_auth import verify_token
from app.firestore.firestore_collections import get_user_ref
from app.services.user_history_service import add_to_history, get_user_history, update_progress
from app.services.user_like_service import add_like, get_user_likes, remove_like
# Temporarily disabled due to import issue
# from app.services.recommendation_service import get_user_recommendations
from app.utils.response_utils import success_response
from datetime import datetime

router = APIRouter()

class OnboardingRequest(BaseModel):
    languages: list = Field(default_factory=list)
    moods: list = Field(default_factory=list)

class PreferencesRequest(BaseModel):
    selected_languages: list = []
    selected_artists: list = []
    selected_moods: list = []
    # Support both naming conventions for compatibility
    languages: list = []
    moods: list = []

class PlayRequest(BaseModel):
    video_id: str = Field(None, alias="videoId")
    id: str = None
    title: str = ""
    artist: str = ""
    thumbnail: str = Field("", alias="thumbnailUrl")
    duration: int = 0
    language: str = ""
    
    def get_video_id(self):
        return self.video_id or self.id

class LikeRequest(BaseModel):
    video_id: str = Field(None, alias="videoId")
    id: str = None
    title: str = ""
    artist: str = ""
    thumbnail: str = Field("", alias="thumbnailUrl")
    duration: int = 0
    language: str = ""
    
    def get_video_id(self):
        return self.video_id or self.id

class ProgressRequest(BaseModel):
    video_id: str = Field(None, alias="videoId")
    id: str = None
    position: int = 0
    duration: int = 0
    
    def get_video_id(self):
        return self.video_id or self.id

@router.get("/onboarding")
async def get_onboarding(token: dict = Depends(verify_token)):
    """
    Get user onboarding status and preferences
    """
    try:
        uid = token["uid"]
        user_ref = get_user_ref(uid)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            preferences = user_data.get('preferences', {})
            return success_response({
                "completed": bool(preferences.get('languages') or preferences.get('moods')),
                "preferences": preferences
            })
        else:
            return success_response({
                "completed": False,
                "preferences": {}
            })
    except Exception as e:
        print(f"Error getting onboarding status: {e}")
        return success_response({
            "completed": False,
            "preferences": {}
        })

@router.post("/onboarding")
async def onboarding(request: OnboardingRequest, token: dict = Depends(verify_token)):
    """
    Handle user onboarding - save language and mood preferences to Firestore
    Called once when user first logs in
    """
    try:
        uid = token["uid"]
        user_ref = get_user_ref(uid)
        
        # Save preferences to Firestore
        user_ref.set({
            'preferences': {
                'languages': request.languages,
                'moods': request.moods,
                'updated_at': datetime.utcnow().isoformat()
            }
        }, merge=True)
        
        return success_response({
            "message": "Onboarding completed successfully",
            "languages": request.languages,
            "moods": request.moods
        })
    except Exception as e:
        print(f"Error in onboarding: {e}")
        return success_response({
            "message": "Onboarding completed with errors"
        })

@router.post("/preferences")
async def save_preferences(request: PreferencesRequest, token: dict = Depends(verify_token)):
    """
    Save user preferences including languages, moods, and artists
    Supports both onboarding and settings updates
    """
    uid = token["uid"]
    user_ref = get_user_ref(uid)
    
    # Merge both naming conventions
    languages = request.selected_languages or request.languages
    moods = request.selected_moods or request.moods
    artists = request.selected_artists
    
    # Build update data
    update_data = {}
    if languages:
        update_data["selected_languages"] = languages
    if moods:
        update_data["selected_moods"] = moods
    if artists:
        update_data["selected_artists"] = artists
    
    # Also save in preferences object for compatibility
    update_data["preferences"] = {
        "languages": languages,
        "moods": moods,
        "artists": artists,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    user_ref.set(update_data, merge=True)
    return success_response({
        "message": "Preferences saved successfully",
        "languages": languages,
        "moods": moods,
        "artists": artists
    }, "Preferences saved")

@router.get("/preferences")
async def get_preferences(token: dict = Depends(verify_token)):
    """
    Get user preferences and onboarding status
    """
    try:
        uid = token["uid"]
        user_ref = get_user_ref(uid)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            preferences = user_data.get('preferences', {})
            return success_response({
                "completed": bool(preferences.get('languages') or preferences.get('moods')),
                "preferences": preferences,
                "selected_languages": user_data.get('selected_languages', []),
                "selected_moods": user_data.get('selected_moods', []),
                "selected_artists": user_data.get('selected_artists', [])
            })
        else:
            return success_response({
                "completed": False,
                "preferences": {},
                "selected_languages": [],
                "selected_moods": [],
                "selected_artists": []
            })
    except Exception as e:
        print(f"Error getting preferences: {e}")
        return success_response({
            "completed": False,
            "preferences": {}
        })

@router.post("/play")
async def track_play(request: PlayRequest, token: dict = Depends(verify_token)):
    try:
        uid = token["uid"]
        video_id = request.get_video_id()
        if not video_id:
            return success_response({}, "Missing video_id but continuing")
        
        data = request.dict(by_alias=True)
        data['video_id'] = video_id
        await add_to_history(uid, data)
        return success_response({}, "Play tracked")
    except Exception as e:
        print(f"Error tracking play: {e}")
        return success_response({}, "Play tracking failed but continuing")

@router.post("/like")
async def like_song(request: LikeRequest, token: dict = Depends(verify_token)):
    try:
        uid = token["uid"]
        video_id = request.get_video_id()
        if not video_id:
            return success_response({}, "Missing video_id but continuing")
        
        data = request.dict(by_alias=True)
        data['video_id'] = video_id
        await add_like(uid, data)
        return success_response({}, "Song liked")
    except Exception as e:
        print(f"Error liking song: {e}")
        return success_response({}, "Like failed but continuing")

@router.post("/progress")
async def save_progress(request: ProgressRequest, token: dict = Depends(verify_token)):
    try:
        uid = token["uid"]
        video_id = request.get_video_id()
        if not video_id:
            return success_response({}, "Missing video_id but continuing")
        
        await update_progress(uid, video_id, request.position, request.duration)
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
