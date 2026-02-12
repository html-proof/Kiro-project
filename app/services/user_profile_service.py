"""
User Profile Service - Comprehensive user data tracking
Stores all user preferences, history, and activity in Firebase Realtime Database
"""
import logging
from datetime import datetime
from typing import Optional, List, Dict
import firebase_admin
from firebase_admin import db

logger = logging.getLogger(__name__)

class UserProfileService:
    def __init__(self):
        self.db_url = "https://sample-music-65323-default-rtdb.asia-southeast1.firebasedatabase.app/"
        
    def _get_user_ref(self, user_id: str):
        """Get Firebase reference for user"""
        return db.reference(f'users/{user_id}', url=self.db_url)
    
    # ==================== USER PREFERENCES ====================
    
    async def set_user_preferences(self, user_id: str, languages: List[str], moods: List[str]):
        """Set user's language and mood preferences (asked once on login)"""
        try:
            user_ref = self._get_user_ref(user_id)
            user_ref.child('preferences').update({
                'languages': languages,
                'moods': moods,
                'updated_at': datetime.utcnow().isoformat()
            })
            logger.info(f"✅ Set preferences for user {user_id}: {len(languages)} languages, {len(moods)} moods")
            return True
        except Exception as e:
            logger.error(f"Failed to set preferences for {user_id}: {e}")
            return False
    
    async def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user's preferences"""
        try:
            user_ref = self._get_user_ref(user_id)
            prefs = user_ref.child('preferences').get()
            return prefs
        except Exception as e:
            logger.error(f"Failed to get preferences for {user_id}: {e}")
            return None
    
    # ==================== SEARCH HISTORY ====================
    
    async def track_search(self, user_id: str, query: str, results_count: int):
        """Track user's search queries"""
        try:
            user_ref = self._get_user_ref(user_id)
            search_ref = user_ref.child('search_history').push()
            search_ref.set({
                'query': query,
                'results_count': results_count,
                'timestamp': datetime.utcnow().isoformat()
            })
            logger.info(f"📝 Tracked search for {user_id}: '{query}'")
            return True
        except Exception as e:
            logger.error(f"Failed to track search for {user_id}: {e}")
            return False
    
    async def get_search_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's recent searches"""
        try:
            user_ref = self._get_user_ref(user_id)
            searches = user_ref.child('search_history').order_by_child('timestamp').limit_to_last(limit).get()
            if searches:
                return [{'id': k, **v} for k, v in searches.items()]
            return []
        except Exception as e:
            logger.error(f"Failed to get search history for {user_id}: {e}")
            return []
    
    # ==================== PLAY HISTORY ====================
    
    async def track_play(self, user_id: str, song_data: Dict):
        """Track when user plays a song"""
        try:
            user_ref = self._get_user_ref(user_id)
            
            # Add to play history
            play_ref = user_ref.child('play_history').push()
            play_ref.set({
                'song_id': song_data.get('id'),
                'title': song_data.get('title'),
                'artist': song_data.get('artist'),
                'duration': song_data.get('duration'),
                'thumbnail': song_data.get('thumbnail'),
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Update play count
            song_stats_ref = user_ref.child(f'song_stats/{song_data.get("id")}')
            current_stats = song_stats_ref.get() or {}
            song_stats_ref.update({
                'play_count': current_stats.get('play_count', 0) + 1,
                'last_played': datetime.utcnow().isoformat(),
                'title': song_data.get('title'),
                'artist': song_data.get('artist')
            })
            
            logger.info(f"▶️ Tracked play for {user_id}: {song_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to track play for {user_id}: {e}")
            return False
    
    async def get_play_history(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Get user's play history"""
        try:
            user_ref = self._get_user_ref(user_id)
            plays = user_ref.child('play_history').order_by_child('timestamp').limit_to_last(limit).get()
            if plays:
                return [{'id': k, **v} for k, v in plays.items()]
            return []
        except Exception as e:
            logger.error(f"Failed to get play history for {user_id}: {e}")
            return []
    
    # ==================== PAUSE/RESUME POSITIONS ====================
    
    async def save_playback_position(self, user_id: str, song_id: str, position_ms: int, duration_ms: int):
        """Save where user paused a song for resume playback"""
        try:
            user_ref = self._get_user_ref(user_id)
            user_ref.child(f'playback_positions/{song_id}').set({
                'position_ms': position_ms,
                'duration_ms': duration_ms,
                'percentage': round((position_ms / duration_ms) * 100, 2) if duration_ms > 0 else 0,
                'updated_at': datetime.utcnow().isoformat()
            })
            logger.info(f"⏸️ Saved position for {user_id}/{song_id}: {position_ms}ms")
            return True
        except Exception as e:
            logger.error(f"Failed to save position for {user_id}/{song_id}: {e}")
            return False
    
    async def get_playback_position(self, user_id: str, song_id: str) -> Optional[Dict]:
        """Get saved playback position for resume"""
        try:
            user_ref = self._get_user_ref(user_id)
            position = user_ref.child(f'playback_positions/{song_id}').get()
            return position
        except Exception as e:
            logger.error(f"Failed to get position for {user_id}/{song_id}: {e}")
            return None
    
    async def clear_playback_position(self, user_id: str, song_id: str):
        """Clear position when song is completed"""
        try:
            user_ref = self._get_user_ref(user_id)
            user_ref.child(f'playback_positions/{song_id}').delete()
            return True
        except Exception as e:
            logger.error(f"Failed to clear position for {user_id}/{song_id}: {e}")
            return False
    
    # ==================== OFFLINE DOWNLOADS ====================
    
    async def track_offline_download(self, user_id: str, song_data: Dict, file_path: str, file_size: int):
        """Track offline downloaded songs"""
        try:
            user_ref = self._get_user_ref(user_id)
            user_ref.child(f'offline_songs/{song_data.get("id")}').set({
                'song_id': song_data.get('id'),
                'title': song_data.get('title'),
                'artist': song_data.get('artist'),
                'duration': song_data.get('duration'),
                'thumbnail': song_data.get('thumbnail'),
                'file_path': file_path,
                'file_size': file_size,
                'quality': song_data.get('quality', 'ultra'),
                'downloaded_at': datetime.utcnow().isoformat()
            })
            logger.info(f"💾 Tracked offline download for {user_id}: {song_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to track offline download for {user_id}: {e}")
            return False
    
    async def get_offline_songs(self, user_id: str) -> List[Dict]:
        """Get list of offline downloaded songs"""
        try:
            user_ref = self._get_user_ref(user_id)
            songs = user_ref.child('offline_songs').get()
            if songs:
                return [{'id': k, **v} for k, v in songs.items()]
            return []
        except Exception as e:
            logger.error(f"Failed to get offline songs for {user_id}: {e}")
            return []
    
    async def remove_offline_song(self, user_id: str, song_id: str):
        """Remove song from offline list"""
        try:
            user_ref = self._get_user_ref(user_id)
            user_ref.child(f'offline_songs/{song_id}').delete()
            logger.info(f"🗑️ Removed offline song for {user_id}: {song_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove offline song for {user_id}/{song_id}: {e}")
            return False
    
    # ==================== USER STATISTICS ====================
    
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get comprehensive user statistics for recommendations"""
        try:
            user_ref = self._get_user_ref(user_id)
            
            # Get all user data
            preferences = user_ref.child('preferences').get() or {}
            song_stats = user_ref.child('song_stats').get() or {}
            play_history = user_ref.child('play_history').order_by_child('timestamp').limit_to_last(100).get() or {}
            search_history = user_ref.child('search_history').order_by_child('timestamp').limit_to_last(50).get() or {}
            offline_songs = user_ref.child('offline_songs').get() or {}
            
            # Calculate statistics
            total_plays = sum(stats.get('play_count', 0) for stats in song_stats.values())
            total_searches = len(search_history)
            total_offline = len(offline_songs)
            
            # Get top played songs
            top_songs = sorted(
                [{'song_id': k, **v} for k, v in song_stats.items()],
                key=lambda x: x.get('play_count', 0),
                reverse=True
            )[:20]
            
            # Get recent searches
            recent_searches = [v.get('query') for v in search_history.values()][-10:]
            
            return {
                'user_id': user_id,
                'preferences': preferences,
                'statistics': {
                    'total_plays': total_plays,
                    'total_searches': total_searches,
                    'total_offline': total_offline,
                    'unique_songs_played': len(song_stats)
                },
                'top_songs': top_songs,
                'recent_searches': recent_searches,
                'languages': preferences.get('languages', []),
                'moods': preferences.get('moods', [])
            }
        except Exception as e:
            logger.error(f"Failed to get stats for {user_id}: {e}")
            return {}
    
    # ==================== RECOMMENDATIONS DATA ====================
    
    async def get_recommendation_data(self, user_id: str) -> Dict:
        """Get all data needed for personalized recommendations"""
        try:
            stats = await self.get_user_stats(user_id)
            
            return {
                'user_id': user_id,
                'languages': stats.get('languages', []),
                'moods': stats.get('moods', []),
                'top_songs': stats.get('top_songs', []),
                'recent_searches': stats.get('recent_searches', []),
                'total_plays': stats.get('statistics', {}).get('total_plays', 0)
            }
        except Exception as e:
            logger.error(f"Failed to get recommendation data for {user_id}: {e}")
            return {}

# Singleton instance
_user_profile_service = None

def get_user_profile_service() -> UserProfileService:
    global _user_profile_service
    if _user_profile_service is None:
        _user_profile_service = UserProfileService()
    return _user_profile_service
