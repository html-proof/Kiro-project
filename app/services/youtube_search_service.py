import yt_dlp
import asyncio
import time
from typing import List, Dict, Any, Optional


class YouTubeService:
    def __init__(self):
        self.ydl_opts_search = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate'
            }
        }
        self.ydl_opts_stream = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'no_color': True,
            'source_address': '0.0.0.0',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate'
            }
        }
        self.stream_cache = {}  # video_id -> {url, info, timestamp}
    
    async def search_songs(self, query: str, limit: int = 10, user_id: str = None) -> List[Dict[str, Any]]:
        """Delegates robust search to specialized SearchService."""
        try:
            return await search_service.search_songs(query, limit, user_id)
        except Exception as e:
            print(f"Error during search delegation: {e}")
            return []
    
    async def get_stream_url(self, video_id: str) -> Dict[str, Any]:
        """Get stream URL with 2-hour caching."""
        loop = asyncio.get_running_loop()
        
        if not video_id:
            print("ERROR: get_stream_url received empty video_id")
            return None
        
        # 1. Check Cache (2 hour TTL)
        now = time.time()
        if video_id in self.stream_cache:
            cache_entry = self.stream_cache[video_id]
            if now - cache_entry['timestamp'] < 7200:  # 2 hours
                print(f"DEBUG: Serving Cached Stream for {video_id}")
                return cache_entry['data']
        
        # 2. Extract fresh URL
        print(f"DEBUG: Extracting stream for: {video_id}")
        
        def _blocking_extract():
            with yt_dlp.YoutubeDL(self.ydl_opts_stream) as ydl:
                url = f"https://www.youtube.com/watch?v={video_id}"
                info = ydl.extract_info(url, download=False)
                return info
        
        try:
            info = await loop.run_in_executor(None, _blocking_extract)
            
            # Get stream URL
            stream_url = info.get('url')
            if not stream_url and 'formats' in info:
                # Fallback: get the first audio-only format
                audio_formats = [
                    f for f in info['formats'] 
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none'
                ]
                if audio_formats:
                    stream_url = audio_formats[0].get('url')
            
            if not stream_url:
                print(f"ERROR: No stream URL found for {video_id}")
                return None
            
            result = {
                "stream_url": stream_url,
                "title": info.get('title'),
                "artist": info.get('uploader'),
                "album": info.get('album') or info.get('title'),
                "thumbnailUrl": info.get('thumbnail')
            }
            
            # Update Cache
            self.stream_cache[video_id] = {
                "data": result,
                "timestamp": now
            }
            
            return result
            
        except Exception as e:
            print(f"Error extracting stream URL for {video_id}: {e}")
            return None
    
    def clear_cache(self):
        """Clear the stream URL cache."""
        self.stream_cache = {}
    
    async def get_artist_details(self, channel_id: str) -> Dict[str, Any]:
        """Fetch artist details and top songs from their channel."""
        loop = asyncio.get_running_loop()
        
        def _blocking_artist_fetch():
            with yt_dlp.YoutubeDL(self.ydl_opts_search) as ydl:
                url = f"https://www.youtube.com/channel/{channel_id}"
                return ydl.extract_info(url, download=False)
        
        try:
            info = await loop.run_in_executor(None, _blocking_artist_fetch)
            entries = info.get('entries', [])
            
            songs = []
            for entry in entries[:20]:
                if not entry:
                    continue
                duration = entry.get('duration', 0)
                if duration and duration < 60:
                    continue
                
                songs.append({
                    "id": entry.get('id'),
                    "title": entry.get('title'),
                    "artist": info.get('uploader') or info.get('title'),
                    "thumbnailUrl": entry.get('thumbnails', [{}])[0].get('url'),
                    "duration": duration
                })
            
            return {
                "id": channel_id,
                "name": info.get('uploader') or info.get('title'),
                "description": info.get('description', ''),
                "thumbnails": info.get('thumbnails', []),
                "songs": songs
            }
            
        except Exception as e:
            print(f"Error fetching artist details: {e}")
            return {"error": str(e)}


class SearchService:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
        }
    
    def normalize(self, text: str) -> str:
        """Normalize text using trusted_channels utility."""
        from app.utils.trusted_channels import trusted_channels
        return trusted_channels.normalize(text)
    
    def contains_negative(self, title: str, query: str) -> bool:
        """Check if title contains spam or non-music content."""
        from app.utils.trusted_channels import trusted_channels
        return trusted_channels.is_spam(title, query)
    
    def get_duration_score(self, seconds: int) -> int:
        """Score based on song duration (penalize too short/long)."""
        if not seconds:
            return 0
        if seconds < 90:
            return -40  # Too short, likely not a full song
        if 120 <= seconds <= 420:
            return 30  # Sweet spot (2-7 minutes)
        if 421 <= seconds <= 600:
            return 10  # Acceptable (7-10 minutes)
        if seconds > 900:
            return -30  # Too long, likely not a song
        return 0
    
    def get_official_score(self, channel: str, title: str) -> int:
        """Calculate trust score for official channels."""
        from app.utils.trusted_channels import trusted_channels
        return trusted_channels.calculate_trust_score(channel, title)
    
    def get_match_score(self, query: str, title: str) -> int:
        """Score based on query-title match quality."""
        q = self.normalize(query)
        t = self.normalize(title)
        score = 0
        
        q_tokens = q.split()
        for token in q_tokens:
            if token in t:
                score += 15
        
        # Bonus for exact phrase match
        if q in t:
            score += 20
        
        return score
    
    def get_personal_context(self, user_id: str) -> Dict[str, Any]:
        """Get user's liked and skipped artists for personalization."""
        if not user_id:
            return {"liked_artists": set(), "skipped_artists": set()}
        
        try:
            from app.firestore.firestore_client import firestore_client
            
            liked = firestore_client.get_liked_songs(user_id)
            
            # Extract artist names from liked songs
            liked_artists = {
                self.normalize(s.get('artist', '')) 
                for s in liked 
                if s.get('artist')
            }
            
            # Skipped artists tracking (placeholder for future implementation)
            skipped_artists = set()
            
            return {
                "liked_artists": liked_artists,
                "skipped_artists": skipped_artists
            }
        except Exception as e:
            print(f"Error getting personal context: {e}")
            return {"liked_artists": set(), "skipped_artists": set()}
    
    async def search_songs(
        self, 
        query: str, 
        limit: int = 10, 
        user_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search for songs with intelligent ranking and personalization.
        
        Args:
            query: Search query string
            limit: Number of results to return
            user_id: Optional user ID for personalized results
            
        Returns:
            List of ranked song results with metadata
        """
        loop = asyncio.get_running_loop()
        
        # 1. Intent Detection (Language-specific search enhancement)
        languages = [
            "malayalam", "hindi", "tamil", "english", "telugu", 
            "kannada", "punjabi", "spanish", "korean"
        ]
        q_norm = self.normalize(query)
        search_query = query
        
        if q_norm in languages:
            search_query = f"{query} songs official audio"
        
        # 2. Get User Context for Personalization
        context = self.get_personal_context(user_id)
        liked_artists = context["liked_artists"]
        skipped_artists = context["skipped_artists"]
        
        # 3. Execute YouTube Search (blocking operation in executor)
        def _blocking_search():
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Fetch more than needed to allow for ranking (Top 40)
                search_results = ydl.extract_info(
                    f"ytsearch40:{search_query}", 
                    download=False
                )
                return search_results.get('entries', [])
        
        try:
            entries = await loop.run_in_executor(None, _blocking_search)
            
            candidates = []
            seen_ids = set()
            seen_titles_durations = []
            
            for entry in entries:
                if not entry or entry.get('id') in seen_ids:
                    continue
                
                title = entry.get('title', '').strip()
                channel = entry.get('uploader', '').strip()
                duration = entry.get('duration', 0)
                view_count = entry.get('view_count', 0)
                
                # Filter spam and non-music content
                if self.contains_negative(title, search_query):
                    continue
                
                # Calculate composite score
                score = 0
                score += self.get_match_score(search_query, title)
                score += self.get_official_score(channel, title)
                score += self.get_duration_score(duration)
                
                # Popularity boost
                if view_count > 10000000:
                    score += 20
                elif view_count > 1000000:
                    score += 10
                
                # --- PERSONALIZATION LAYER ---
                c_norm = self.normalize(channel)
                
                if c_norm in liked_artists:
                    score += 50  # Massive boost for favorite artists
                
                if c_norm in skipped_artists:
                    score -= 100  # Heavy penalty for skipped artists
                # -----------------------------
                
                # Duplicate detection (similar titles with similar duration)
                is_duplicate = False
                lower_title = title.lower()
                
                for existing_title, existing_duration in seen_titles_durations:
                    ed_raw = existing_duration or 0
                    if (lower_title in existing_title or existing_title in lower_title) and \
                       abs(duration - ed_raw) < 5:
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    continue
                
                # Build result object
                candidates.append({
                    "id": entry.get('id'),
                    "title": title,
                    "artist": channel,
                    "channelId": entry.get('uploader_id'),
                    "duration": duration,
                    "thumbnailUrl": entry.get('thumbnails', [{}])[0].get('url'),
                    "album": entry.get('album'),
                    "score": score
                })
                
                seen_ids.add(entry.get('id'))
                seen_titles_durations.append((lower_title, duration))
            
            # Sort by score and return top results
            candidates.sort(key=lambda x: x['score'], reverse=True)
            return candidates[:limit]
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []


# Export singletons
search_service = SearchService()
yt_service = YouTubeService()


# Convenience function for backward compatibility
async def search_youtube(query: str, limit: int = 10, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Main search function with intelligent filtering and personalization.
    Uses the trusted_channels filter to block spam and non-music content.
    """
    return await search_service.search_songs(query, limit, user_id)
