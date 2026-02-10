import yt_dlp
from app.utils.quality_utils import select_best_video_format
from app.redis.redis_cache import cache_set, cache_get

async def resolve_video_stream(video_id: str, quality: str = "low") -> dict:
    cache_key = f"video:{video_id}:{quality}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best"
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            formats = info.get("formats", [])
            
            best_format = select_best_video_format(formats, quality)
            
            if best_format:
                result = {
                    "stream_url": best_format.get("url"),
                    "resolution": f"{best_format.get('height', 360)}p",
                    "format": best_format.get("ext", "mp4")
                }
                cache_set(cache_key, result, 900)
                return result
    except Exception as e:
        return None
