import re

BLOCKED_KEYWORDS = [
    "news", "politics", "interview", "speech", "shorts", "ytshorts", "reels", 
    "memes", "movie", "trailer", "comedy", "8d", "3d", "slowed", "reverb",
    "remix", "nightcore", "bass boosted", "status", "lyrical video", "live stream",
    "full movie"
]

def is_valid_music_result(result: dict) -> bool:
    title = result.get("title", "").lower()
    uploader = result.get("uploader", "").lower()
    duration = result.get("duration", 0)
    
    # Duration check
    if duration < 60 or duration > 720:
        return False
    
    # Keyword check
    for keyword in BLOCKED_KEYWORDS:
        if keyword in title or keyword in uploader:
            return False
    
    # Prefer music category
    if result.get("categories") and "Music" in result.get("categories"):
        return True
    
    return True

def filter_music_results(results: list) -> list:
    return [r for r in results if is_valid_music_result(r)]
