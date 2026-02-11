import re

BLOCKED_KEYWORDS = [
    # News / politics / talk (non-podcast)
    "news", "politics", "debate", "election", "press", "conference",
    "interview", "interview clip", "press meet", "breaking",

    # Shorts / reels / social junk
    "shorts", "ytshorts", "reels", "instagram", "facebook",
    "tiktok", "snapchat", "status", "story",

    # Movies / series / visuals
    "movie", "full movie", "trailer", "teaser", "scene",
    "web series", "episode", "netflix", "prime video", "hotstar",

    # Comedy / skits / reactions
    "comedy", "standup", "stand-up", "skit", "spoof",
    "parody", "funny", "reaction", "roast",

    # Visual edits / effects
    "8d", "3d", "4k", "hd", "hdr",
    "edit", "fan edit", "amv", "gmv",
    "visualizer", "aesthetic", "loop",

    # Audio-destroying edits
    "slowed", "slowed + reverb", "reverb", "nightcore",
    "remix", "mashup", "mix", "dj",
    "bass boosted", "trap", "phonk", "lofi remix",

    # Low-quality / spam
    "full album", "megahit", "nonstop",
    "1 hour", "2 hours", "10 hours",
    "playlist", "collection", "jukebox",

    # Lyrics / text videos
    "lyrics", "lyrical", "lyric video", "subtitles", "karaoke",

    # Live / stage / crowd noise
    "live", "live stream", "concert", "performance",
    "stage show", "audience", "cover", "tribute",

    # AI / fake content
    "ai cover", "ai voice", "deepfake",
    "voice clone", "ai generated",

    # Clickbait / cringe
    "viral", "trend", "challenge", "prank",
    "emotional", "goosebumps", "must watch",

    # Religious / speeches (unless you want them)
    "speech", "sermon", "pravachan", "motivational",
    "bhajan", "aarti", "chant", "mantra",

    # ----------------------------
    # Adult / Porn / Sex (BLOCK)
    # ----------------------------
    "porn", "porno", "pornhub", "xvideos", "xnxx", "onlyfans",
    "sex", "sexy", "xxx", "adult", "18+", "nsfw",
    "nude", "nudes", "naked", "nudity",
    "blowjob", "handjob", "anal", "hardcore", "erotic",
    "hookup", "escort", "prostitute", "brothel",

    # ----------------------------
    # Rape / Abuse (BLOCK)
    # ----------------------------
    "rape", "raped", "rapist", "molest", "molestation",
    "sexual assault", "harassment", "incest",

    # ----------------------------
    # Violence / Murder / Weapons (BLOCK)
    # ----------------------------
    "kill", "killing", "murder", "murdered", "assassination",
    "shoot", "shooting", "gun", "pistol", "rifle",
    "knife", "stab", "stabbing", "bomb", "blast", "explosion",
    "massacre", "blood", "gore", "torture", "beheading",

    # ----------------------------
    # Drugs (BLOCK)
    # ----------------------------
    "cocaine", "heroin", "weed", "marijuana", "ganja",
    "meth", "lsd", "ecstasy", "mdma", "drug deal", "drug dealer",

    # ----------------------------
    # Terrorism / Extremism (BLOCK)
    # ----------------------------
    "terror", "terrorist", "terrorism", "isis", "islamic state",
    "al qaeda", "taliban", "jihad", "extremist",
    "bombing", "suicide bomb", "hostage",

    # ----------------------------
    # Illegal / Crime (BLOCK)
    # ----------------------------
    "crime", "criminal", "robbery", "steal", "stolen",
    "kidnap", "kidnapping", "hijack", "fraud", "scam",

    # ----------------------------
    # Extra strong dark terms (optional but useful)
    # ----------------------------
    "dead", "death", "suicide", "self harm",
    "war", "riot", "genocide"
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
