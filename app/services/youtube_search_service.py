import yt_dlp
from app.utils.filter_utils import filter_music_results
from app.redis.redis_cache import cache_set, cache_get

async def search_youtube(query: str, limit: int = 15) -> list:
    cache_key = f"search:{query}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "default_search": "ytsearch15"
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            entries = result.get("entries", [])
            
            results = []
            for entry in entries:
                results.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "artist": entry.get("uploader"),
                    "thumbnail": entry.get("thumbnail"),
                    "duration": entry.get("duration", 0)
                })
            
            filtered = filter_music_results(results)
            cache_set(cache_key, filtered, 300)
            return filtered
    except Exception as e:
        return []
