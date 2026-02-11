import yt_dlp
import logging
from app.utils.quality_utils import get_bitrate_for_quality, select_best_audio_format
from app.redis.redis_cache import cache_set, cache_get

logger = logging.getLogger(__name__)

async def resolve_audio_stream(video_id: str, quality: str = "saver") -> dict:
    cache_key = f"stream:{video_id}:{quality}"
    cached = cache_get(cache_key)
    if cached:
        logger.debug(f"Cache hit for audio stream: {video_id}")
        return cached
    
    target_bitrate = get_bitrate_for_quality(quality)
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best"
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            formats = info.get("formats", [])
            
            if not formats:
                logger.error(f"No formats available for video: {video_id}")
                return None
            
            best_format = select_best_audio_format(formats, target_bitrate)
            
            if not best_format:
                logger.error(f"No suitable audio format found for video: {video_id}")
                return None
            
            result = {
                "stream_url": best_format.get("url"),
                "bitrate": best_format.get("abr", target_bitrate),
                "format": best_format.get("ext", "m4a")
            }
            cache_set(cache_key, result, 900)
            logger.info(f"Resolved audio stream for {video_id}: {result['bitrate']}kbps {result['format']}")
            return result
    except Exception as e:
        logger.error(f"Failed to resolve audio stream for {video_id}: {e}")
        return None
