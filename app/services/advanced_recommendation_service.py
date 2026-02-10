from typing import List, Dict, Any, Optional
import random
from app.firestore.firestore_client import firestore_client
from app.services.youtube_search_service import search_service, yt_service
from app.services.ml_recommender_service import ml_recommender


class AdvancedRecommendationService:
    """
    Advanced recommendation service with multiple strategies:
    1. ML-based collaborative filtering (ALS)
    2. Content-based similarity (TF-IDF)
    3. Artist-based recommendations
    4. Trending fallback
    
    All recommendations use the trusted_channels filter for quality.
    """
    
    async def get_personalized_recommendations(
        self, 
        user_id: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get personalized recommendations using hybrid approach.
        
        Strategy:
        1. Try ML (ALS) recommendations first
        2. Fallback to artist-based recommendations
        3. Fill with trending if needed
        """
        recommendations = []
        seen_ids = set()
        
        # Get user's liked songs to avoid duplicates
        try:
            user_likes = firestore_client.get_liked_songs(user_id)
            for s in user_likes:
                seen_ids.add(s.get('id') or s.get('video_id'))
        except Exception as e:
            print(f"Error fetching user likes: {e}")
        
        # 1. Try ML (ALS) Recommendations First
        try:
            ml_results = ml_recommender.get_als_recommendations(user_id, n=15)
            
            for vid in ml_results:
                # Enrich ML data with full metadata via search
                res = await search_service.search_songs(vid, limit=1, user_id=user_id)
                if res and res[0]['id'] not in seen_ids:
                    recommendations.append(res[0])
                    seen_ids.add(res[0]['id'])
                    
            print(f"ML recommendations: {len(recommendations)}")
            
        except Exception as e:
            print(f"ML Rec failed, falling back: {e}")
        
        # 2. Strategy A: Based on Favorite Artists (Classical Fallback)
        if len(recommendations) < limit:
            try:
                top_artists = firestore_client.get_frequent_artists(user_id, limit=10)
                
                if top_artists:
                    for i, artist in enumerate(top_artists):
                        if len(recommendations) >= limit:
                            break
                        
                        fetch_limit = 10 if i == 0 else 5
                        results = await search_service.search_songs(
                            f"best of {artist}", 
                            limit=fetch_limit,
                            user_id=user_id
                        )
                        
                        for song in results:
                            if song['id'] not in seen_ids:
                                recommendations.append(song)
                                seen_ids.add(song['id'])
                                
                                if len(recommendations) >= limit:
                                    break
                    
                    print(f"After artist-based: {len(recommendations)}")
                    
            except Exception as e:
                print(f"Error in artist-based recommendations: {e}")
        
        # 3. Strategy B: Fill with trending/new if needed
        if len(recommendations) < limit:
            needed = limit - len(recommendations)
            fillers = await search_service.search_songs(
                "latest music hits 2024", 
                limit=needed + 10,
                user_id=user_id
            )
            
            for song in fillers:
                if song['id'] not in seen_ids:
                    recommendations.append(song)
                    seen_ids.add(song['id'])
                    
                    if len(recommendations) >= limit:
                        break
            
            print(f"After trending fill: {len(recommendations)}")
        
        return recommendations[:limit]
    
    async def get_daily_mix(self, user_id: str, limit: int = 12) -> List[Dict[str, Any]]:
        """
        Generate a daily mix based on user's top artists.
        """
        try:
            top_artists = firestore_client.get_frequent_artists(user_id, limit=30)
            
            if not top_artists:
                return await search_service.search_songs(
                    "lofi chill beats for study", 
                    limit=limit,
                    user_id=user_id
                )
            
            primary_artist = top_artists[0]
            results = await search_service.search_songs(
                f"{primary_artist} essential mix", 
                limit=limit,
                user_id=user_id
            )
            
            return results
            
        except Exception as e:
            print(f"Error in daily mix: {e}")
            return []
    
    async def get_recent_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get recommendations based on recently played song.
        Uses ML content similarity first, then keyword search.
        """
        try:
            history = firestore_client.get_play_history(user_id, limit=1)
            
            if not history:
                return {"last_song": None, "recommendations": []}
            
            last_song = history[0]
            video_id = last_song.get('video_id')
            
            recommendations = []
            seen_ids = {video_id}
            
            # 1. Try Content-Based ML Similarity First
            ml_results = ml_recommender.get_content_similarity(video_id, n=8)
            
            if ml_results:
                for vid in ml_results:
                    res = await search_service.search_songs(
                        vid, 
                        limit=1,
                        user_id=user_id
                    )
                    if res and res[0]['id'] not in seen_ids:
                        recommendations.append(res[0])
                        seen_ids.add(res[0]['id'])
            
            # 2. Fallback to Keyword Search
            if len(recommendations) < 8:
                search_query = f"songs similar to {last_song.get('title')} {last_song.get('artist')}"
                results = await search_service.search_songs(
                    search_query, 
                    limit=12,
                    user_id=user_id
                )
                
                for s in results:
                    if s['id'] not in seen_ids:
                        recommendations.append(s)
                        seen_ids.add(s['id'])
            
            return {
                "last_song": last_song,
                "recommendations": recommendations[:12]
            }
            
        except Exception as e:
            print(f"Error in context rec: {e}")
            return {"last_song": None, "recommendations": []}
    
    async def get_autoplay_next(
        self, 
        user_id: str, 
        current_song_id: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find the best next songs for autoplay based on history and similarity.
        """
        try:
            # 1. Get user context
            top_artists = firestore_client.get_frequent_artists(user_id, limit=30)
            history = firestore_client.get_play_history(user_id, limit=20)
            
            seen_ids = {current_song_id}
            for h in history:
                vid = h.get('video_id') or h.get('id')
                if vid:
                    seen_ids.add(vid)
            
            # 2. Try similarity search for current song
            current_info = await yt_service.get_stream_url(current_song_id)
            
            if current_info:
                query = f"songs similar to {current_info.get('title')} {current_info.get('artist')}"
                sim_results = await search_service.search_songs(
                    query, 
                    limit=5,
                    user_id=user_id
                )
                
                candidates = [s for s in sim_results if s['id'] not in seen_ids]
                if candidates:
                    return candidates[:limit]
            
            # 3. Fallback to favorite artists
            if top_artists:
                artist = random.choice(top_artists[:3])
                artist_results = await search_service.search_songs(
                    f"{artist} top songs audio", 
                    limit=5,
                    user_id=user_id
                )
                
                candidates = [s for s in artist_results if s['id'] not in seen_ids]
                if candidates:
                    return candidates[:limit]
            
            # 4. Ultimate fallback
            return await search_service.search_songs(
                "top hits global 2024", 
                limit=limit,
                user_id=user_id
            )
            
        except Exception as e:
            print(f"Autoplay Error: {e}")
            return []
    
    async def get_similar_songs(
        self, 
        song_id: str, 
        user_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get songs similar to a given song using content-based filtering.
        """
        try:
            # Try ML content similarity first
            ml_results = ml_recommender.get_content_similarity(song_id, n=limit)
            
            recommendations = []
            seen_ids = {song_id}
            
            for vid in ml_results:
                res = await search_service.search_songs(
                    vid, 
                    limit=1,
                    user_id=user_id
                )
                if res and res[0]['id'] not in seen_ids:
                    recommendations.append(res[0])
                    seen_ids.add(res[0]['id'])
            
            # If not enough, use search-based similarity
            if len(recommendations) < limit:
                song_info = await yt_service.get_stream_url(song_id)
                if song_info:
                    query = f"{song_info.get('title')} {song_info.get('artist')} similar"
                    search_results = await search_service.search_songs(
                        query,
                        limit=limit,
                        user_id=user_id
                    )
                    
                    for s in search_results:
                        if s['id'] not in seen_ids:
                            recommendations.append(s)
                            seen_ids.add(s['id'])
            
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Error getting similar songs: {e}")
            return []
    
    async def get_artist_radio(
        self, 
        artist_name: str, 
        user_id: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Create a radio station based on an artist.
        """
        try:
            # Get artist's top songs
            results = await search_service.search_songs(
                f"{artist_name} top songs official audio",
                limit=limit,
                user_id=user_id
            )
            
            return results
            
        except Exception as e:
            print(f"Error creating artist radio: {e}")
            return []


# Export singleton
advanced_recommendation_service = AdvancedRecommendationService()
