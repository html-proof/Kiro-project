from fastapi import APIRouter, Query
from app.services.youtube_search_service import search_youtube
from app.utils.query_builder_utils import build_youtube_search_query
from app.utils.response_utils import success_response

router = APIRouter()

@router.get("/type")
async def recommend_by_type(type: str = Query(...), language: str = Query("English")):
    query = build_youtube_search_query("", language, type)
    results = await search_youtube(query, limit=20)
    return success_response(results)

@router.get("/artist")
async def recommend_by_artist(name: str = Query(...), language: str = Query("English")):
    query = f"{name} {language} songs"
    results = await search_youtube(query, limit=20)
    return success_response(results)

@router.get("/similar")
async def recommend_similar(id: str = Query(...)):
    # Simplified: search for similar content
    results = await search_youtube(f"similar songs", limit=15)
    return success_response(results)

@router.get("/because-liked")
async def recommend_because_liked():
    results = await search_youtube("popular songs", limit=15)
    return success_response(results)
