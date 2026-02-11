def get_bitrate_for_quality(quality: str) -> int:
    quality_map = {
        "ultra": 48,
        "saver": 64,
        "high": 128
    }
    return quality_map.get(quality, 64)

def select_best_audio_format(formats: list, target_bitrate: int):
    # Prefer audio-only formats, but fall back to combined formats if needed
    audio_only = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") == "none"]
    audio_with_video = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"]
    
    # Try audio-only first
    audio_formats = audio_only if audio_only else audio_with_video
    
    if not audio_formats:
        return None
    
    best = None
    best_diff = float('inf')
    
    for fmt in audio_formats:
        abr = fmt.get("abr", 0) or fmt.get("tbr", 0)
        if abr == 0:
            continue
            
        diff = abs(abr - target_bitrate)
        if diff < best_diff:
            best = fmt
            best_diff = diff
    
    return best

def select_best_video_format(formats: list, quality: str):
    # Filter for formats with both video AND audio
    video_formats = [f for f in formats 
                     if f.get("vcodec") != "none" 
                     and f.get("acodec") != "none"
                     and f.get("height", 0) > 0]
    
    # If no combined formats, fall back to video-only
    if not video_formats:
        video_formats = [f for f in formats if f.get("vcodec") != "none" and f.get("height", 0) > 0]
    
    if not video_formats:
        return None
    
    height_map = {"low": 360, "medium": 480, "high": 720}
    target_height = height_map.get(quality, 360)
    
    best = None
    best_diff = float('inf')
    
    for fmt in video_formats:
        height = fmt.get("height", 0)
        diff = abs(height - target_height)
        
        if diff < best_diff:
            best = fmt
            best_diff = diff
    
    return best
