from app.services.youtube_search_service import search_youtube
from app.services.user_like_service import get_user_likes
from app.services.user_history_service import get_user_history
from app.services.user_profile_service import get_user_profile_service
from app.utils.query_builder_utils import build_youtube_search_query
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)
profile_service = get_user_profile_service()

def _filter_already_played(results: list, played_song_ids: set) -> list:
    """Filter out songs user has already played"""
    filtered = [song for song in results if song.get('id') not in played_song_ids]
    logger.info(f"🔍 Filtered {len(results) - len(filtered)} already played songs")
    return filtered

def _get_daily_seed(uid: str) -> int:
    """Generate consistent seed for today's date per user"""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    seed_string = f"{uid}_{today}"
    return hash(seed_string) % 10000

async def get_user_recommendations(uid: str) -> list:
    """
    Get personalized "For You" recommendations based on:
    - User's language preferences
    - User's mood preferences
    - Top played songs (for similarity)
    - Recent searches
    - FILTERED: Excludes already played songs
    """
    try:
        # Get comprehensive user data
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data or not user_data.get('languages'):
            # No profile data, return popular songs
            logger.info(f"No profile data for {uid}, returning popular songs")
            return await search_youtube("popular songs 2026", limit=30)
        
        # Get played song IDs for filtering
        play_history = await profile_service.get_play_history(uid, limit=200)
        played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
        logger.info(f"📊 User {uid} has played {len(played_song_ids)} unique songs")
        
        # Build personalized query based on user preferences
        languages = user_data.get('languages', [])
        moods = user_data.get('moods', [])
        top_songs = user_data.get('top_songs', [])
        recent_searches = user_data.get('recent_searches', [])
        
        # Try multiple query variations to get fresh content
        all_results = []
        
        # Query 1: Language + Mood + "new songs"
        if languages and moods:
            query = f"{languages[0]} {moods[0]} new songs 2026"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Query 2: Language + different mood
        if languages and len(moods) > 1:
            query = f"{languages[0]} {moods[1]} latest songs"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Query 3: Similar to top song but exclude exact match
        if top_songs:
            top_song_artist = top_songs[0].get('artist', '')
            if top_song_artist:
                query = f"{top_song_artist} {languages[0] if languages else ''} songs"
                results = await search_youtube(query, limit=15, user_id=uid)
                all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Query 4: Based on recent search but with "new" keyword
        if recent_searches:
            query = f"{recent_searches[0]} new releases"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Deduplicate by song ID
        seen_ids = set()
        unique_results = []
        for song in all_results:
            if song.get('id') not in seen_ids:
                seen_ids.add(song.get('id'))
                unique_results.append(song)
        
        # Shuffle for variety
        random.shuffle(unique_results)
        
        logger.info(f"🎯 For You: {len(unique_results)} NEW songs for {uid}")
        return unique_results[:20]
        
    except Exception as e:
        logger.error(f"Failed to get personalized recommendations for {uid}: {e}")
        # Fallback to popular songs
        return await search_youtube("popular songs 2026", limit=30)

async def get_daily_mix(uid: str) -> list:
    """
    Get "Daily Mix" - Changes every day with fresh songs
    - Uses daily seed for consistent results per day
    - Filters out already played songs
    - Mixes user preferences with discovery
    """
    try:
        # Get user data
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data:
            return await search_youtube("trending music 2026", limit=30)
        
        # Get played song IDs for filtering
        play_history = await profile_service.get_play_history(uid, limit=200)
        played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
        
        # Get daily seed for consistent results today
        daily_seed = _get_daily_seed(uid)
        random.seed(daily_seed)
        
        languages = user_data.get('languages', [])
        moods = user_data.get('moods', [])
        top_songs = user_data.get('top_songs', [])
        
        all_results = []
        
        # Mix 1: Random mood from user preferences
        if moods:
            random_mood = random.choice(moods)
            query = f"{languages[0] if languages else ''} {random_mood} songs"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Mix 2: Discover new artists in user's language
        if languages:
            query = f"{languages[0]} new artists 2026"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Mix 3: Similar to a random top song
        if top_songs and len(top_songs) > 2:
            random_top = random.choice(top_songs[:5])
            query = f"{random_top.get('artist', '')} similar artists"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Mix 4: Trending in user's language
        if languages:
            query = f"{languages[0]} trending now"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Deduplicate
        seen_ids = set()
        unique_results = []
        for song in all_results:
            if song.get('id') not in seen_ids:
                seen_ids.add(song.get('id'))
                unique_results.append(song)
        
        # Shuffle with daily seed
        random.seed(daily_seed)
        random.shuffle(unique_results)
        
        logger.info(f"🎵 Daily Mix: {len(unique_results)} NEW songs for {uid} (seed: {daily_seed})")
        return unique_results[:20]
        
    except Exception as e:
        logger.error(f"Failed to get daily mix for {uid}: {e}")
        return await search_youtube("trending music 2026", limit=30)

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
    Get "Because You Liked" recommendations
    - Based on top played songs
    - Filters out already played songs
    - Discovers similar new content
    """
    try:
        # Get user's top songs and preferences
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data:
            return await search_youtube("trending music 2026", limit=30)
        
        # Get played song IDs for filtering
        play_history = await profile_service.get_play_history(uid, limit=200)
        played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
        
        top_songs = user_data.get('top_songs', [])
        languages = user_data.get('languages', [])
        moods = user_data.get('moods', [])
        
        all_results = []
        
        if not top_songs:
            # No play history, use preferences only
            query_parts = []
            if languages:
                query_parts.append(languages[0])
            if moods:
                query_parts.append(moods[0])
            query_parts.append("trending songs")
            query = " ".join(query_parts)
            results = await search_youtube(query, limit=20, user_id=uid)
            return _filter_already_played(results, played_song_ids)
        
        # Get similar songs for top 3 played songs
        for i, song in enumerate(top_songs[:3]):
            artist = song.get('artist', '')
            title = song.get('title', '')
            
            if artist:
                # Search for similar artists
                query = f"{artist} similar songs {languages[0] if languages else ''}"
                results = await search_youtube(query, limit=15, user_id=uid)
                all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Deduplicate
        seen_ids = set()
        unique_results = []
        for song in all_results:
            if song.get('id') not in seen_ids:
                seen_ids.add(song.get('id'))
                unique_results.append(song)
        
        # Shuffle for variety
        random.shuffle(unique_results)
        
        logger.info(f"💝 Because You Liked: {len(unique_results)} NEW songs for {uid}")
        return unique_results[:20]
        
    except Exception as e:
        logger.error(f"Failed to get 'because you liked' for {uid}: {e}")
        return await search_youtube("trending music 2026", limit=30)

async def get_mood_based_recommendations(uid: str, mood: str) -> list:
    """
    Get recommendations based on specific mood
    - Filters out already played songs
    """
    try:
        user_data = await profile_service.get_recommendation_data(uid)
        languages = user_data.get('languages', []) if user_data else []
        
        # Get played song IDs for filtering
        play_history = await profile_service.get_play_history(uid, limit=200)
        played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
        
        query_parts = []
        if languages:
            query_parts.append(languages[0])
        query_parts.append(mood)
        query_parts.append("new songs")
        
        query = " ".join(query_parts)
        logger.info(f"😊 Mood-based query for {uid}: {query}")
        
        results = await search_youtube(query, limit=30, user_id=uid)
        filtered_results = _filter_already_played(results, played_song_ids)
        
        return filtered_results[:20]
        
    except Exception as e:
        logger.error(f"Failed to get mood recommendations for {uid}: {e}")
        return await search_youtube(f"{mood} songs", limit=20)

async def get_discover_weekly(uid: str) -> list:
    """
    Get "Discover Weekly" - Fresh discoveries based on taste
    - Completely new songs user hasn't heard
    - Based on listening patterns
    - Changes weekly
    """
    try:
        user_data = await profile_service.get_recommendation_data(uid)
        
        if not user_data:
            return await search_youtube("new music releases", limit=20)
        
        # Get played song IDs for filtering
        play_history = await profile_service.get_play_history(uid, limit=200)
        played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
        
        languages = user_data.get('languages', [])
        top_songs = user_data.get('top_songs', [])
        
        all_results = []
        
        # Discover 1: New releases in user's language
        if languages:
            query = f"{languages[0]} new releases this week"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Discover 2: Indie/underground in user's language
        if languages:
            query = f"{languages[0]} indie songs 2026"
            results = await search_youtube(query, limit=15, user_id=uid)
            all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Discover 3: Similar artists to top played
        if top_songs:
            for song in top_songs[:2]:
                artist = song.get('artist', '')
                if artist:
                    query = f"artists like {artist}"
                    results = await search_youtube(query, limit=5, user_id=uid)
                    all_results.extend(_filter_already_played(results, played_song_ids))
        
        # Deduplicate
        seen_ids = set()
        unique_results = []
        for song in all_results:
            if song.get('id') not in seen_ids:
                seen_ids.add(song.get('id'))
                unique_results.append(song)
        
        random.shuffle(unique_results)
        
        logger.info(f"🔍 Discover Weekly: {len(unique_results)} NEW songs for {uid}")
        return unique_results[:20]
        
    except Exception as e:
        logger.error(f"Failed to get discover weekly for {uid}: {e}")
        return await search_youtube("new music releases", limit=20)
