from app.services.youtube_search_service import search_youtube
from app.services.user_like_service import get_user_likes
from app.services.user_history_service import get_user_history
from app.utils.query_builder_utils import build_youtube_search_query

async def get_user_recommendations(uid: str) -> list:
    """Get personalized recommendations based on user's listening history and likes"""
    # Try to get user's liked songs and history for better recommendations
    try:
        likes = await get_user_likes(uid, limit=5)
        if likes:
            # Use first liked song to find similar content
            first_like = likes[0]
            query = f"{first_like.get('title', '')} similar songs"
            results = await search_youtube(query, limit=20)
            return results
    except:
        pass
    
    # Fallback to popular songs
    results = await search_youtube("popular songs 2024", limit=20)
    return results

async def get_recommendations_by_artist(artist_name: str, language: str = "English") -> list:
    """Get recommendations for a specific artist"""
    query = build_youtube_search_query(artist_name, language, "")
    results = await search_youtube(query, limit=20)
    return results

async def get_similar_songs(video_id: str, uid: str = None) -> list:
    """Get songs similar to the specified video"""
    # In a real implementation, you'd fetch the video details first
    # For now, we'll return popular songs as a fallback
    results = await search_youtube("popular music", limit=20)
    return results

async def get_because_you_liked_recommendations(uid: str) -> list:
    """Get recommendations based on user's liked songs"""
    try:
        likes = await get_user_likes(uid, limit=10)
        if not likes:
            # No likes yet, return popular songs
            return await search_youtube("trending music 2024", limit=20)
        
        # Build a query from liked songs
        titles = [like.get('title', '') for like in likes[:3]]
        query = f"{' '.join(titles)} similar songs"
        results = await search_youtube(query, limit=20)
        return results
    except Exception as e:
        # Fallback to popular songs
        results = await search_youtube("trending music 2024", limit=20)
        return results
