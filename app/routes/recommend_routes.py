from fastapi import APIRouter, Query, Depends
from app.services import youtube_search_service, recommendation_service
from app.utils.query_builder_utils import build_youtube_search_query
from app.utils.response_utils import success_response
from app.firebase.firebase_auth import verify_token

router = APIRouter()

@router.get("/type")
async def recommend_by_type(type: str = Query(...), language: str = Query("")):
    """Get recommendations by music type (e.g., pop, rock, jazz)"""
    # If no language specified, use trending query without language filter
    if not language or language.strip() == "":
        query = f"{type} trending songs"
    else:
        query = build_youtube_search_query("", language, type)
    results = await youtube_search_service.search_youtube(query, limit=20)
    return success_response(results)

@router.get("/artist")
async def recommend_by_artist(name: str = Query(...), language: str = Query("")):
    """Get recommendations for a specific artist"""
    # If no language specified, search without language filter
    if not language or language.strip() == "":
        language = None
    results = await recommendation_service.get_recommendations_by_artist(name, language or "")
    return success_response(results)

@router.get("/similar")
async def recommend_similar(
    id: str = Query(..., description="Video ID to find similar songs for"),
    user: dict = Depends(verify_token)
):
    """Get songs similar to the specified video"""
    uid = user.get("uid")
    results = await recommendation_service.get_similar_songs(id, uid)
    return success_response(results)

@router.get("/for-you")
async def get_for_you(uid: str = Query(...)):
    """
    Get "For You" recommendations
    - Based on user history and preferences
    - Filters out already played songs
    - Fresh content discovery
    """
    results = await recommendation_service.get_user_recommendations(uid)
    return success_response(results)

@router.get("/daily-mix")
async def get_daily_mix(uid: str = Query(...)):
    """
    Get "Daily Mix" - Changes every day
    - Consistent results per day
    - Filters out already played songs
    - Mix of preferences and discovery
    """
    results = await recommendation_service.get_daily_mix(uid)
    return success_response(results)

@router.get("/because-liked")
async def recommend_because_liked(uid: str = Query(...)):
    """
    Get "Because You Liked" recommendations
    - Based on top played songs
    - Filters out already played songs
    - Similar content discovery
    """
    results = await recommendation_service.get_because_you_liked_recommendations(uid)
    return success_response(results)

@router.get("/discover-weekly")
async def get_discover_weekly(uid: str = Query(...)):
    """
    Get "Discover Weekly" recommendations
    - Fresh discoveries based on taste
    - Completely new songs
    - Changes weekly
    """
    results = await recommendation_service.get_discover_weekly(uid)
    return success_response(results)

@router.get("/mood")
async def get_mood_recommendations(
    uid: str = Query(...),
    mood: str = Query(...)
):
    """
    Get mood-based recommendations
    - Filters out already played songs
    - Based on user's language preference
    """
    results = await recommendation_service.get_mood_based_recommendations(uid, mood)
    return success_response(results)

@router.get("/personalized")
async def get_personalized_recommendations(user: dict = Depends(verify_token)):
    """Get personalized recommendations based on user's listening history and likes"""
    uid = user.get("uid")
    results = await recommendation_service.get_user_recommendations(uid)
    return success_response(results)
