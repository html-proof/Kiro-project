from fastapi import APIRouter, Query
from app.services.youtube_search_service import search_youtube
from app.utils.trusted_channels import trusted_channels
from app.utils.response_utils import success_response
from typing import Optional
import random

router = APIRouter()

@router.get("/channels")
async def get_trusted_channels():
    """
    Get list of all trusted music channels organized by category.
    """
    return success_response({
        "global_labels": trusted_channels.GLOBAL_LABELS,
        "indian_labels": trusted_channels.INDIAN_LABELS,
        "east_asian_labels": trusted_channels.EAST_ASIAN_LABELS,
        "regional_labels": trusted_channels.REGIONAL_LABELS,
        "live_music_labels": trusted_channels.LIVE_MUSIC_LABELS,
        "total_channels": len(trusted_channels.ALL_TRUSTED)
    })

@router.get("/recommendations")
async def get_trusted_channel_recommendations(
    query: Optional[str] = Query(None, description="Search query (movie name, album, artist, etc.)"),
    language: Optional[str] = Query(None, description="Filter by language (malayalam, hindi, tamil, etc.)"),
    limit: int = Query(20, description="Number of songs to return"),
    user_id: Optional[str] = Query(None)
):
    """
    Get song recommendations from trusted channels only.
    
    - If query is provided (e.g., "Kathi"), searches for songs from that movie/album
    - Filters by language if specified
    - Only returns songs from Topic channels and official labels
    - Guaranteed spam-free results
    
    Examples:
    - /trusted/recommendations?query=kathi&language=tamil
    - /trusted/recommendations?query=leo&language=tamil
    - /trusted/recommendations?language=malayalam (random Malayalam songs)
    """
    
    # Language-specific channel mapping
    language_channels = {
        "malayalam": [
            "manorama music", "muzik247", "satyam audios", "millennium audios",
            "jax music", "swargachitra", "century music", "sony music malayalam",
            "malayalam cassettes"
        ],
        "hindi": [
            "t-series", "zee music", "saregama", "tips official",
            "yrf", "times music", "sony music india"
        ],
        "tamil": [
            "saregama tamil", "think music india", "d imman music", "sowkya music",
            "sony music south", "lahari music tamil"
        ],
        "telugu": [
            "aditya music", "volga video", "ananda audio", "larsc entertainment",
            "sony music south"
        ],
        "kannada": [
            "lahari music", "anand audio", "paramvah studios", "msil music"
        ],
        "punjabi": [
            "speed records", "white hill music", "jass records", "djjass records",
            "r-nation", "fresh touch entertainment", "mp4 music", "b ally music"
        ],
        "marathi": [
            "zee music marathi", "tips marathi", "shree ashtavinayak", "atharva entertainment"
        ],
        "bengali": [
            "svf music", "times music bangla", "shree venkatesh films", "grassroot entertainment"
        ]
    }
    
    # Build search query based on input
    if query:
        # User provided specific query (movie name, album, etc.)
        search_query = query
        
        # Add language context if provided
        if language:
            search_query = f"{query} {language} songs"
        
        # Add "official audio" or "topic" for better results
        search_query = f"{search_query} official audio"
        
        print(f"🎬 Movie/Album search: {search_query}")
        
    elif language and language.lower() in language_channels:
        # No query, but language specified - get random songs from trusted channels
        channels = language_channels[language.lower()]
        selected_channel = random.choice(channels)
        search_query = f"{language} songs {selected_channel}"
        
        print(f"🎵 Language-based search: {search_query}")
        
    elif language:
        # Generic language search
        search_query = f"{language} songs official audio"
        
        print(f"🎵 Generic language search: {search_query}")
        
    else:
        # No query, no language - mix of popular songs
        popular_queries = [
            "trending songs official audio",
            "latest music official audio",
            "top hits official audio"
        ]
        search_query = random.choice(popular_queries)
        
        print(f"🎵 Random popular search: {search_query}")
    
    # Search with trusted channel filter
    results = await search_youtube(search_query, limit=limit * 2, user_id=user_id)  # Get more to filter
    
    # Additional filter: Only keep results from trusted channels
    trusted_results = []
    for song in results:
        channel = song.get('artist', '').lower()
        title = song.get('title', '').lower()
        
        # Check if from trusted channel or Topic channel
        is_trusted = any(label in channel for label in trusted_channels.ALL_TRUSTED)
        is_topic = " - topic" in channel or "- topic" in channel
        
        # If query provided, check if title matches the query (movie/album name)
        query_match = True
        if query:
            query_lower = query.lower()
            # Check if query keywords appear in title
            query_words = query_lower.split()
            title_words = title.split()
            
            # At least one word from query should match title
            query_match = any(word in title_words for word in query_words if len(word) > 2)
        
        if (is_trusted or is_topic) and query_match:
            song['verified'] = True
            song['channel_type'] = 'topic' if is_topic else 'trusted'
            song['source'] = 'trusted_channels'
            trusted_results.append(song)
        
        # Stop when we have enough results
        if len(trusted_results) >= limit:
            break
    
    # If we have query but no results, try without strict matching
    if query and len(trusted_results) < 5:
        print(f"⚠️ Few results for '{query}', trying broader search...")
        
        # Try again with just the query + language
        if language:
            fallback_query = f"{query} {language}"
        else:
            fallback_query = query
        
        fallback_results = await search_youtube(fallback_query, limit=limit, user_id=user_id)
        
        for song in fallback_results:
            if song.get('id') not in [s.get('id') for s in trusted_results]:
                channel = song.get('artist', '').lower()
                is_trusted = any(label in channel for label in trusted_channels.ALL_TRUSTED)
                is_topic = " - topic" in channel or "- topic" in channel
                
                if is_trusted or is_topic:
                    song['verified'] = True
                    song['channel_type'] = 'topic' if is_topic else 'trusted'
                    song['source'] = 'trusted_channels_fallback'
                    trusted_results.append(song)
                    
                    if len(trusted_results) >= limit:
                        break
    
    return success_response({
        "songs": trusted_results[:limit],
        "query": query,
        "language": language,
        "total": len(trusted_results[:limit]),
        "source": "trusted_channels_only"
    })

@router.get("/by-channel")
async def get_songs_by_channel(
    channel: str = Query(..., description="Channel name (e.g., 'manorama music', 't-series')"),
    limit: int = Query(20, description="Number of songs to return"),
    user_id: Optional[str] = Query(None)
):
    """
    Get songs from a specific trusted channel.
    """
    
    # Verify channel is trusted
    channel_lower = channel.lower()
    is_trusted = any(label in channel_lower for label in trusted_channels.ALL_TRUSTED)
    
    if not is_trusted:
        return {
            "success": False,
            "message": f"Channel '{channel}' is not in trusted channels list"
        }
    
    # Search for songs from this channel
    search_query = f"{channel} official audio"
    results = await search_youtube(search_query, limit=limit, user_id=user_id)
    
    # Filter to only include songs from the requested channel
    channel_results = []
    for song in results:
        song_channel = song.get('artist', '').lower()
        if channel_lower in song_channel:
            song['verified'] = True
            channel_results.append(song)
    
    return success_response({
        "songs": channel_results,
        "channel": channel,
        "total": len(channel_results),
        "verified": True
    })

@router.get("/featured")
async def get_featured_channels(
    category: Optional[str] = Query(None, description="Category: global, indian, regional, live")
):
    """
    Get featured channels by category with sample songs.
    """
    
    category_map = {
        "global": trusted_channels.GLOBAL_LABELS[:10],
        "indian": trusted_channels.INDIAN_LABELS[:15],
        "regional": trusted_channels.REGIONAL_LABELS[:10],
        "live": trusted_channels.LIVE_MUSIC_LABELS[:10]
    }
    
    if category and category.lower() in category_map:
        channels = category_map[category.lower()]
    else:
        # Mix of all categories
        channels = (
            trusted_channels.GLOBAL_LABELS[:5] +
            trusted_channels.INDIAN_LABELS[:10] +
            trusted_channels.REGIONAL_LABELS[:5]
        )
    
    featured = []
    for channel in channels:
        featured.append({
            "name": channel,
            "category": category or "mixed",
            "verified": True
        })
    
    return success_response({
        "channels": featured,
        "category": category or "mixed",
        "total": len(featured)
    })
