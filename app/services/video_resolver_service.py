import yt_dlp
import logging
from app.utils.quality_utils import select_best_video_format
from app.redis.redis_cache import cache_set, cache_get

logger = logging.getLogger(__name__)

async def resolve_video_stream(video_id: str, quality: str = "low") -> dict:
    cache_key = f"video:{video_id}:{quality}"
    cached = cache_get(cache_key)
    if cached:
        logger.debug(f"Cache hit for video stream: {video_id}")
        return cached
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
                "player_skip": ["webpage", "configs"]
            }
        },
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            formats = info.get("formats", [])
            
            if not formats:
                logger.error(f"No formats available for video: {video_id}")
                return None
            
            best_format = select_best_video_format(formats, quality)
            
            if not best_format:
                logger.error(f"No suitable video format found for video: {video_id}")
                return None
            
            result = {
                "stream_url": best_format.get("url"),
                "resolution": f"{best_format.get('height', 360)}p",
                "format": best_format.get("ext", "mp4"),
                "has_audio": best_format.get("acodec") != "none"
            }
            cache_set(cache_key, result, 900)
            logger.info(f"Resolved video stream for {video_id}: {result['resolution']} {result['format']} (audio: {result['has_audio']})")
            return result
    except Exception as e:
        logger.error(f"Failed to resolve video stream for {video_id}: {e}")
        return None
