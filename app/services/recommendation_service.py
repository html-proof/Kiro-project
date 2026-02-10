from app.services.youtube_search_service import search_youtube

async def get_user_recommendations(uid: str) -> list:
    # Simplified recommendation - just return popular songs
    results = await search_youtube("popular songs 2024", limit=20)
    return results
