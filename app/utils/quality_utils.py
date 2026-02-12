def get_bitrate_for_quality(quality: str) -> int:
    quality_map = {
        "ultra": 48,      # Ultra low for data saving
        "saver": 64,      # Low quality for data saving
        "medium": 128,    # Medium quality
        "high": 192,      # High quality
        "max": 999        # Maximum available quality (will select highest)
    }
    return quality_map.get(quality, 128)

def select_best_audio_format(formats: list, target_bitrate: int):
    # 🔥 PRIORITY 1: FORCE itag=140 (m4a, 128kbps) - Most stable for mobile
    # This is the most reliable format for ExoPlayer/just_audio
    itag_140 = [f for f in formats if f.get("format_id") == "140"]
    if itag_140:
        return itag_140[0]
    
    # 🔥 PRIORITY 2: Any M4A audio-only format
    # M4A is more reliable than WEBM for mobile playback
    m4a_formats = [f for f in formats 
                   if f.get("acodec") != "none" 
                   and f.get("vcodec") == "none"
                   and f.get("ext") == "m4a"]
    
    # If no M4A, try any audio-only format (but prefer m4a/mp4 over webm)
    if not m4a_formats:
        audio_only = [f for f in formats 
                      if f.get("acodec") != "none" 
                      and f.get("vcodec") == "none"]
        # Sort by extension preference: m4a > mp4 > opus > webm
        ext_priority = {"m4a": 0, "mp4": 1, "opus": 2, "webm": 3}
        audio_only.sort(key=lambda f: ext_priority.get(f.get("ext", ""), 99))
        m4a_formats = audio_only
    
    # Last resort: any format with audio
    if not m4a_formats:
        m4a_formats = [f for f in formats if f.get("acodec") != "none"]
    
    if not m4a_formats:
        return None
    
    # If target is 999 (max quality), just get the highest bitrate
    if target_bitrate >= 999:
        best = None
        max_bitrate = 0
        for fmt in m4a_formats:
            abr = fmt.get("abr", 0) or fmt.get("tbr", 0)
            if abr > max_bitrate:
                max_bitrate = abr
                best = fmt
        return best
    
    # Otherwise, find closest to target
    best = None
    best_diff = float('inf')
    
    for fmt in m4a_formats:
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
