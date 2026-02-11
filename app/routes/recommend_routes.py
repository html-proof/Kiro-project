from fastapi import APIRouter, Query, Depends
from app.services import youtube_search_service, recommendation_service
from app.utils.query_builder_utils import build_youtube_search_query
from app.utils.response_utils import success_response
from app.firebase.firebase_auth import verify_token

router = APIRouter()

@router.get("/type")
async def recommend_by_type(type: str = Query(...), language: str = Query("English")):
    """Get recommendations by music type (e.g., pop, rock, jazz)"""
    query = build_youtube_search_query("", language, type)
    results = await youtube_search_service.search_youtube(query, limit=20)
    return success_response(results)

@router.get("/artist")
async def recommend_by_artist(name: str = Query(...), language: str = Query("English")):
    """Get recommendations for a specific artist"""
    results = await recommendation_service.get_recommendations_by_artist(name, language)
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

@router.get("/because-liked")
async def recommend_because_liked(user: dict = Depends(verify_token)):
    """Get recommendations based on user's liked songs"""
    uid = user.get("uid")
    results = await recommendation_service.get_because_you_liked_recommendations(uid)
    return success_response(results)

@router.get("/personalized")
async def get_personalized_recommendations(user: dict = Depends(verify_token)):
    """Get personalized recommendations based on user's listening history and likes"""
    uid = user.get("uid")
    results = await recommendation_service.get_user_recommendations(uid)
    return success_response(results)
