import yt_dlp
import logging
import os
from app.utils.quality_utils import get_bitrate_for_quality, select_best_audio_format
from app.redis.redis_cache import cache_set, cache_get

logger = logging.getLogger(__name__)

# Check if cookies file exists
COOKIES_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'cookies.txt')
USE_COOKIES = os.path.exists(COOKIES_FILE)

async def resolve_audio_stream(video_id: str, quality: str = "ultra") -> dict:
    cache_key = f"stream:{video_id}:{quality}"
    cached = cache_get(cache_key)
    if cached:
        logger.info(f"⚡ Cache hit for audio stream: {video_id} - INSTANT!")
        return cached
    
    logger.info(f"🔍 Resolving {video_id} (not in cache, will take 2-5s)")
    target_bitrate = get_bitrate_for_quality(quality)
    
    # Try with multiple strategies - OPTIMIZED FOR SPEED
    strategies = [
        # Strategy 1: ULTRA FAST - iOS Client (often fastest & most reliable)
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "skip_download": True,
            "no_check_certificate": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["ios", "android", "web"],
                    "player_skip": ["webpage", "configs", "js"],
                    "skip": ["hls", "dash"]
                }
            },
        },
        # Strategy 2: Android Client (Reliable fallback)
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "skip_download": True,
            "no_check_certificate": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                    "player_skip": ["webpage", "configs", "js"],
                    "skip": ["hls", "dash"]
                }
            },
        },
        # Strategy 3: Web Client (Last resort)
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web"],
                    "player_skip": ["webpage"]
                }
            },
        }
    ]
    
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.5",
        "Sec-Fetch-Mode": "navigate"
    }
    
    last_error = None
    
    for i, ydl_opts in enumerate(strategies):
        ydl_opts["http_headers"] = base_headers
        
        # Add cookies if available
        if USE_COOKIES:
            ydl_opts["cookiefile"] = COOKIES_FILE
        
        try:
            logger.debug(f"Trying strategy {i+1} for {video_id}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                formats = info.get("formats", [])
                
                if not formats:
                    logger.warning(f"No formats available for video: {video_id} (strategy {i+1})")
                    continue
                
                best_format = select_best_audio_format(formats, target_bitrate)
                
                if not best_format:
                    logger.warning(f"No suitable audio format found for video: {video_id} (strategy {i+1})")
                    continue
                
                result = {
                    "stream_url": best_format.get("url"),
                    "bitrate": best_format.get("abr", target_bitrate),
                    "format": best_format.get("ext", "m4a")
                }
                
                # Cache for 4 HOURS (URLs typically valid for 6 hours)
                cache_set(cache_key, result, 14400)
                logger.info(f"✅ Resolved audio stream for {video_id}: {result['bitrate']}kbps {result['format']} (strategy {i+1}) - cached for 4h")
                return result
                
        except Exception as e:
            last_error = e
            logger.warning(f"Strategy {i+1} failed for {video_id}: {e}")
            continue
    
    # All strategies failed
    logger.error(f"Failed to resolve audio stream for {video_id} after {len(strategies)} attempts: {last_error}")
    return None

# Background resolver for pre-caching
import asyncio
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=5)

async def resolve_audio_stream_background(video_id: str, quality: str = "ultra"):
    """Resolve stream URL in background without blocking"""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(_executor, _resolve_sync, video_id, quality)
    except Exception as e:
        logger.error(f"Background resolution failed for {video_id}: {e}")

def _resolve_sync(video_id: str, quality: str):
    """Synchronous resolver for background execution"""
    cache_key = f"stream:{video_id}:{quality}"
    
    # Check cache first
    if cache_get(cache_key):
        return
    
    target_bitrate = get_bitrate_for_quality(quality)
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
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
    
    if USE_COOKIES:
        ydl_opts["cookiefile"] = COOKIES_FILE
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            formats = info.get("formats", [])
            
            if formats:
                best_format = select_best_audio_format(formats, target_bitrate)
                if best_format:
                    result = {
                        "stream_url": best_format.get("url"),
                        "bitrate": best_format.get("abr", target_bitrate),
                        "format": best_format.get("ext", "m4a")
                    }
                    cache_set(cache_key, result, 900)
                    logger.info(f"🔄 Background resolved: {video_id}")
    except Exception as e:
        logger.error(f"Background resolution error for {video_id}: {e}")
