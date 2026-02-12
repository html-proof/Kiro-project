from app.services.youtube_search_service import search_youtube
from app.services.user_like_service import get_user_likes
from app.services.user_history_service import get_user_history
from app.services.user_profile_service import get_user_profile_service
from app.utils.query_builder_utils import build_youtube_search_query
import logging

logger = logging.getLogger(__name__)
profile_service = get_user_profile_service()

async def get_user_recommendations(uid: str) -> list:
    """
    Get personalized recommendations based on:
    - User's language preferences
    - User's mood preferences
    - Top played songs
    - Recent searches
    - Play history
    """
    try:
        # Get comprehensive user data
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data or not user_data.get('languages'):
            # No profile data, return popular songs
            logger.info(f"No profile data for {uid}, returning popular songs")
            return await search_youtube("popular songs 2024", limit=20)
        
        # Build personalized query based on user preferences
        languages = user_data.get('languages', [])
        moods = user_data.get('moods', [])
        top_songs = user_data.get('top_songs', [])
        recent_searches = user_data.get('recent_searches', [])
        
        # Combine preferences into search query
        query_parts = []
        
        # Add language preference
        if languages:
            query_parts.append(languages[0])  # Primary language
        
        # Add mood preference
        if moods:
            query_parts.append(moods[0])  # Primary mood
        
        # Add "songs" keyword
        query_parts.append("songs")
        
        # If user has top songs, use them for similarity
        if top_songs:
            top_song_title = top_songs[0].get('title', '')
            if top_song_title:
                query_parts.append(f"like {top_song_title}")
        
        query = " ".join(query_parts)
        logger.info(f"🎯 Personalized query for {uid}: {query}")
        
        results = await search_youtube(query, limit=20, user_id=uid)
        return results
        
    except Exception as e:
        logger.error(f"Failed to get personalized recommendations for {uid}: {e}")
        # Fallback to popular songs
        return await search_youtube("popular songs 2024", limit=20)

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
    """
    Get recommendations based on user's top played songs and preferences
    """
    try:
        # Get user's top songs and preferences
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data:
            return await search_youtube("trending music 2024", limit=20)
        
        top_songs = user_data.get('top_songs', [])
        languages = user_data.get('languages', [])
        moods = user_data.get('moods', [])
        
        if not top_songs:
            # No play history, use preferences only
            query_parts = []
            if languages:
                query_parts.append(languages[0])
            if moods:
                query_parts.append(moods[0])
            query_parts.append("trending songs")
            query = " ".join(query_parts)
        else:
            # Build query from top played songs
            top_titles = [song.get('title', '') for song in top_songs[:3]]
            query = f"{' '.join(top_titles)} similar songs"
        
        logger.info(f"💝 Because you liked query for {uid}: {query}")
        results = await search_youtube(query, limit=20, user_id=uid)
        return results
        
    except Exception as e:
        logger.error(f"Failed to get 'because you liked' for {uid}: {e}")
        return await search_youtube("trending music 2024", limit=20)

async def get_mood_based_recommendations(uid: str, mood: str) -> list:
    """
    Get recommendations based on specific mood
    """
    try:
        user_data = await profile_service.get_recommendation_data(uid)
        languages = user_data.get('languages', []) if user_data else []
        
        query_parts = []
        if languages:
            query_parts.append(languages[0])
        query_parts.append(mood)
        query_parts.append("songs")
        
        query = " ".join(query_parts)
        logger.info(f"😊 Mood-based query for {uid}: {query}")
        
        results = await search_youtube(query, limit=20, user_id=uid)
        return results
        
    except Exception as e:
        logger.error(f"Failed to get mood recommendations for {uid}: {e}")
        return await search_youtube(f"{mood} songs", limit=20)
