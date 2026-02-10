def get_bitrate_for_quality(quality: str) -> int:
    quality_map = {
        "ultra": 48,
        "saver": 64,
        "high": 128
    }
    return quality_map.get(quality, 64)

def select_best_audio_format(formats: list, target_bitrate: int):
    audio_formats = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") == "none"]
    if not audio_formats:
        audio_formats = [f for f in formats if f.get("acodec") != "none"]
    
    best = None
    for fmt in audio_formats:
        abr = fmt.get("abr", 0) or fmt.get("tbr", 0)
        if not best or abs(abr - target_bitrate) < abs(best.get("abr", 0) - target_bitrate):
            best = fmt
    
    return best

def select_best_video_format(formats: list, quality: str):
    video_formats = [f for f in formats if f.get("vcodec") != "none"]
    
    height_map = {"low": 360, "medium": 480, "high": 720}
    target_height = height_map.get(quality, 360)
    
    best = None
    for fmt in video_formats:
        height = fmt.get("height", 0)
        if not best or abs(height - target_height) < abs(best.get("height", 0) - target_height):
            best = fmt
    
    return best
