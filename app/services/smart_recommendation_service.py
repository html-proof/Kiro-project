"""
Smart Recommendation Service
Continuously searches and recommends audio based on:
- User mood preferences
- Current date and time (morning/afternoon/evening/night)
- Trusted YouTube channels
- View counts and popularity
- User listening history
"""

import logging
from datetime import datetime, time
from typing import List, Dict, Optional
import random

from app.services.youtube_search_service import search_youtube
from app.services.user_profile_service import get_user_profile_service
from app.utils.trusted_channels import trusted_channels

logger = logging.getLogger(__name__)
profile_service = get_user_profile_service()


class SmartRecommendationService:
    """Advanced recommendation engine with time-aware and view-based filtering"""
    
    # Time-based mood mapping
    TIME_MOODS = {
        'morning': ['Energetic', 'Happy', 'Motivational', 'Workout', 'Upbeat'],
        'afternoon': ['Focus', 'Chill', 'Relaxing', 'Romantic', 'Smooth'],
        'evening': ['Party', 'Dance', 'Upbeat', 'Romantic', 'Energetic'],
        'night': ['Chill', 'Relaxing', 'Sad', 'Romantic', 'Calm']
    }
    
    # Mood to search keywords mapping
    MOOD_KEYWORDS = {
        'Happy': ['happy', 'cheerful', 'upbeat', 'feel good', 'positive'],
        'Sad': ['sad', 'emotional', 'heartbreak', 'melancholy', 'soulful'],
        'Energetic': ['energetic', 'power', 'pump up', 'high energy', 'intense'],
        'Relaxing': ['relaxing', 'calm', 'peaceful', 'soothing', 'ambient'],
        'Romantic': ['romantic', 'love', 'heart', 'valentine', 'couple'],
        'Party': ['party', 'dance', 'club', 'edm', 'celebration'],
        'Workout': ['workout', 'gym', 'fitness', 'training', 'exercise'],
        'Focus': ['focus', 'study', 'concentration', 'work', 'productivity'],
        'Chill': ['chill', 'lofi', 'laid back', 'easy listening', 'mellow'],
        'Motivational': ['motivational', 'inspiring', 'powerful', 'epic', 'uplifting'],
        'Dance': ['dance', 'groove', 'beat', 'rhythm', 'moves'],
        'Acoustic': ['acoustic', 'unplugged', 'live', 'stripped', 'raw'],
        'Electronic': ['electronic', 'edm', 'techno', 'house', 'synth'],
        'Rock': ['rock', 'metal', 'alternative', 'indie rock', 'hard rock'],
        'Pop': ['pop', 'mainstream', 'chart', 'hit', 'popular'],
        'Classical': ['classical', 'orchestra', 'symphony', 'instrumental', 'piano'],
        'Jazz': ['jazz', 'smooth jazz', 'blues', 'swing', 'saxophone'],
        'Hip-Hop': ['hip hop', 'rap', 'trap', 'urban', 'beats']
    }
    
    # Minimum view counts for quality filtering
    MIN_VIEWS = {
        'high_quality': 1_000_000,    # 1M+ views
        'medium_quality': 100_000,     # 100K+ views
        'emerging': 10_000             # 10K+ views
    }
    
    def __init__(self):
        self.trusted_channels = trusted_channels
    
    def _get_time_of_day(self) -> str:
        """Determine current time of day"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            return 'morning'
        elif 12 <= current_hour < 17:
            return 'afternoon'
        elif 17 <= current_hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def _get_current_date_context(self) -> Dict[str, any]:
        """Get current date context for recommendations"""
        now = datetime.now()
        return {
            'year': now.year,
            'month': now.strftime('%B'),
            'month_num': now.month,
            'day': now.day,
            'weekday': now.strftime('%A'),
            'time_of_day': self._get_time_of_day(),
            'is_weekend': now.weekday() >= 5,
            'season': self._get_season(now.month)
        }
    
    def _get_season(self, month: int) -> str:
        """Get current season"""
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'
    
    def _get_time_appropriate_moods(self, user_moods: List[str]) -> List[str]:
        """Filter user moods based on current time of day"""
        time_of_day = self._get_time_of_day()
        time_moods = self.TIME_MOODS.get(time_of_day, [])
        
        # Prioritize moods that match current time
        appropriate_moods = [mood for mood in user_moods if mood in time_moods]
        
        # If no match, return all user moods
        if not appropriate_moods:
            appropriate_moods = user_moods
        
        logger.info(f"⏰ Time: {time_of_day} | Appropriate moods: {appropriate_moods}")
        return appropriate_moods
    
    def _build_smart_query(
        self, 
        language: Optional[str], 
        mood: str, 
        date_context: Dict
    ) -> str:
        """Build intelligent search query based on context"""
        query_parts = []
        
        # Add language if specified
        if language:
            query_parts.append(language)
        
        # Add mood keywords (pick random for variety)
        mood_keywords = self.MOOD_KEYWORDS.get(mood, [mood.lower()])
        selected_keyword = random.choice(mood_keywords)
        query_parts.append(selected_keyword)
        
        # Add temporal context
        if date_context['is_weekend']:
            query_parts.append('weekend')
        
        # Add trending keywords based on time
        if date_context['month_num'] in [11, 12]:  # Holiday season
            query_parts.append('hits')
        else:
            query_parts.append(f"trending {date_context['month']} {date_context['year']}")
        
        # Add "official" to prefer official releases
        query_parts.append('official')
        
        query = ' '.join(query_parts)
        logger.info(f"🔍 Smart query: {query}")
        return query
    
    def _filter_by_views(
        self, 
        results: List[Dict], 
        min_views: int = None
    ) -> List[Dict]:
        """Filter results by view count"""
        if min_views is None:
            min_views = self.MIN_VIEWS['emerging']
        
        filtered = []
        for song in results:
            views = song.get('views', 0)
            
            # Convert view string to number if needed
            if isinstance(views, str):
                views = self._parse_view_count(views)
            
            if views >= min_views:
                filtered.append(song)
        
        logger.info(f"📊 Filtered by views (min: {min_views:,}): {len(results)} → {len(filtered)}")
        return filtered
    
    def _parse_view_count(self, view_str: str) -> int:
        """Parse view count string to integer"""
        if not view_str:
            return 0
        
        view_str = view_str.lower().replace(',', '').replace(' ', '')
        
        try:
            if 'k' in view_str:
                return int(float(view_str.replace('k', '')) * 1_000)
            elif 'm' in view_str:
                return int(float(view_str.replace('m', '')) * 1_000_000)
            elif 'b' in view_str:
                return int(float(view_str.replace('b', '')) * 1_000_000_000)
            else:
                return int(view_str)
        except:
            return 0
    
    def _filter_by_trusted_channels(
        self, 
        results: List[Dict], 
        min_trust_score: int = 30
    ) -> List[Dict]:
        """Filter results by trusted channels"""
        filtered = []
        for song in results:
            channel = song.get('channel', '')
            title = song.get('title', '')
            
            trust_score = self.trusted_channels.calculate_trust_score(channel, title)
            
            if trust_score >= min_trust_score:
                song['trust_score'] = trust_score
                filtered.append(song)
        
        logger.info(f"🏆 Filtered by trust (min: {min_trust_score}): {len(results)} → {len(filtered)}")
        return filtered
    
    def _remove_spam(self, results: List[Dict], query: str) -> List[Dict]:
        """Remove spam and non-music content"""
        filtered = []
        for song in results:
            title = song.get('title', '')
            if not self.trusted_channels.is_spam(title, query):
                filtered.append(song)
        
        logger.info(f"🚫 Removed spam: {len(results)} → {len(filtered)}")
        return filtered
    
    def _sort_by_quality(self, results: List[Dict]) -> List[Dict]:
        """Sort results by quality score (trust + views)"""
        def quality_score(song):
            trust = song.get('trust_score', 0)
            views = song.get('views', 0)
            if isinstance(views, str):
                views = self._parse_view_count(views)
            
            # Normalize views to 0-100 scale
            view_score = min(100, (views / 10_000_000) * 100)
            
            # Combined score: 60% trust, 40% views
            return (trust * 0.6) + (view_score * 0.4)
        
        sorted_results = sorted(results, key=quality_score, reverse=True)
        logger.info(f"📈 Sorted by quality score")
        return sorted_results
    
    async def get_smart_recommendations(
        self, 
        uid: str, 
        limit: int = 30,
        quality_level: str = 'medium_quality'
    ) -> List[Dict]:
        """
        Get smart recommendations based on:
        - User mood preferences
        - Current time of day
        - Current date/season
        - Trusted channels
        - View counts
        """
        try:
            # Get user profile
            user_data = await profile_service.get_recommendation_data(uid)
            
            if not user_data or not user_data.get('moods'):
                logger.warning(f"⚠️ No user data for {uid}, using defaults")
                return await self._get_default_recommendations(quality_level, limit)
            
            # Get date context
            date_context = self._get_current_date_context()
            logger.info(f"📅 Context: {date_context['time_of_day']} {date_context['weekday']}, {date_context['month']} {date_context['year']}")
            
            # Get user preferences
            languages = user_data.get('languages', [])
            user_moods = user_data.get('moods', [])
            
            # Filter moods by time of day
            appropriate_moods = self._get_time_appropriate_moods(user_moods)
            
            # Get played songs for filtering
            play_history = await profile_service.get_play_history(uid, limit=200)
            played_song_ids = {play.get('song_id') for play in play_history if play.get('song_id')}
            
            all_results = []
            
            # Search for each appropriate mood
            for mood in appropriate_moods[:3]:  # Limit to top 3 moods
                for language in (languages[:2] if languages else [None]):  # Top 2 languages
                    # Build smart query
                    query = self._build_smart_query(language, mood, date_context)
                    
                    # Search YouTube
                    results = await search_youtube(query, limit=20, user_id=uid)
                    
                    # Apply filters
                    results = self._remove_spam(results, query)
                    results = self._filter_by_trusted_channels(results, min_trust_score=30)
                    results = self._filter_by_views(results, self.MIN_VIEWS[quality_level])
                    
                    # Filter already played
                    results = [s for s in results if s.get('id') not in played_song_ids]
                    
                    all_results.extend(results)
            
            # Deduplicate by song ID
            seen_ids = set()
            unique_results = []
            for song in all_results:
                if song.get('id') not in seen_ids:
                    seen_ids.add(song.get('id'))
                    unique_results.append(song)
            
            # Sort by quality
            unique_results = self._sort_by_quality(unique_results)
            
            logger.info(f"✨ Smart recommendations: {len(unique_results)} high-quality songs for {uid}")
            return unique_results[:limit]
            
        except Exception as e:
            logger.error(f"❌ Smart recommendations failed for {uid}: {e}")
            return await self._get_default_recommendations(quality_level, limit)
    
    async def _get_default_recommendations(
        self, 
        quality_level: str, 
        limit: int
    ) -> List[Dict]:
        """Get default recommendations when user data is unavailable"""
        date_context = self._get_current_date_context()
        time_of_day = date_context['time_of_day']
        
        # Get time-appropriate moods
        default_moods = self.TIME_MOODS.get(time_of_day, ['Happy', 'Energetic'])
        
        query = f"{default_moods[0]} trending {date_context['month']} {date_context['year']} official"
        results = await search_youtube(query, limit=limit * 2)
        
        # Apply filters
        results = self._remove_spam(results, query)
        results = self._filter_by_trusted_channels(results, min_trust_score=30)
        results = self._filter_by_views(results, self.MIN_VIEWS[quality_level])
        results = self._sort_by_quality(results)
        
        return results[:limit]
    
    async def get_continuous_feed(
        self, 
        uid: str, 
        page: int = 1, 
        page_size: int = 20
    ) -> Dict:
        """
        Get continuous feed of recommendations
        Supports pagination for infinite scroll
        """
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get smart recommendations (fetch more than needed)
            all_recommendations = await self.get_smart_recommendations(
                uid, 
                limit=page_size * 3,  # Fetch 3x to ensure enough after filtering
                quality_level='medium_quality'
            )
            
            # Paginate
            paginated = all_recommendations[offset:offset + page_size]
            
            has_more = len(all_recommendations) > offset + page_size
            
            return {
                'songs': paginated,
                'page': page,
                'page_size': page_size,
                'total': len(paginated),
                'has_more': has_more,
                'context': self._get_current_date_context()
            }
            
        except Exception as e:
            logger.error(f"❌ Continuous feed failed for {uid}: {e}")
            return {
                'songs': [],
                'page': page,
                'page_size': page_size,
                'total': 0,
                'has_more': False,
                'error': str(e)
            }


# Export singleton
smart_recommendation_service = SmartRecommendationService()
