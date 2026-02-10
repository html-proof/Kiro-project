from app.firestore.firestore_collections import (
    get_auto_playlists_ref, get_auto_playlist_songs_ref,
    get_user_history_ref, get_user_likes_ref
)
from app.utils.time_utils import now_timestamp, days_ago
from collections import Counter

async def generate_on_repeat(uid: str):
    history_ref = get_user_history_ref(uid)
    thirty_days_ago = days_ago(30)
    
    docs = history_ref.where("played_at", ">=", thirty_days_ago).stream()
    
    video_counts = Counter()
    video_data = {}
    
    for doc in docs:
        data = doc.to_dict()
        vid = data.get("video_id")
        video_counts[vid] += 1
        if vid not in video_data:
            video_data[vid] = data
    
    top_30 = video_counts.most_common(30)
    
    playlist_id = "on_repeat"
    auto_ref = get_auto_playlists_ref(uid)
    auto_ref.document(playlist_id).set({
        "playlist_id": playlist_id,
        "name": "On Repeat",
        "description": "Your most played songs",
        "type": "on_repeat",
        "tags": ["mix", "auto"],
        "created_at": now_timestamp(),
        "updated_at": now_timestamp()
    })
    
    songs_ref = get_auto_playlist_songs_ref(uid, playlist_id)
    for vid, count in top_30:
        if vid in video_data:
            song = video_data[vid]
            song["score"] = count
            song["added_at"] = now_timestamp()
            songs_ref.document(vid).set(song)

async def generate_daily_mix(uid: str):
    # Mix of favorites and trending
    playlist_id = "daily_mix"
    auto_ref = get_auto_playlists_ref(uid)
    auto_ref.document(playlist_id).set({
        "playlist_id": playlist_id,
        "name": "Daily Mix",
        "description": "Your personalized mix",
        "type": "daily_mix",
        "tags": ["mix", "auto"],
        "created_at": now_timestamp(),
        "updated_at": now_timestamp()
    })

async def generate_recently_played(uid: str):
    history_ref = get_user_history_ref(uid)
    docs = history_ref.order_by("played_at", direction="DESCENDING").limit(50).stream()
    
    playlist_id = "recently_played"
    auto_ref = get_auto_playlists_ref(uid)
    auto_ref.document(playlist_id).set({
        "playlist_id": playlist_id,
        "name": "Recently Played",
        "description": "Your recent listening history",
        "type": "recently_played",
        "tags": ["history", "auto"],
        "created_at": now_timestamp(),
        "updated_at": now_timestamp()
    })
    
    songs_ref = get_auto_playlist_songs_ref(uid, playlist_id)
    for doc in docs:
        song = doc.to_dict()
        song["added_at"] = now_timestamp()
        songs_ref.document(song["video_id"]).set(song)

async def generate_liked_songs(uid: str):
    likes_ref = get_user_likes_ref(uid)
    docs = likes_ref.order_by("liked_at", direction="DESCENDING").stream()
    
    playlist_id = "liked_songs"
    auto_ref = get_auto_playlists_ref(uid)
    auto_ref.document(playlist_id).set({
        "playlist_id": playlist_id,
        "name": "Liked Songs",
        "description": "All your liked songs",
        "type": "liked_songs",
        "tags": ["favorites", "auto"],
        "created_at": now_timestamp(),
        "updated_at": now_timestamp()
    })
    
    songs_ref = get_auto_playlist_songs_ref(uid, playlist_id)
    for doc in docs:
        song = doc.to_dict()
        song["added_at"] = now_timestamp()
        songs_ref.document(song["video_id"]).set(song)

async def regenerate_all_auto_playlists(uid: str):
    await generate_on_repeat(uid)
    await generate_daily_mix(uid)
    await generate_recently_played(uid)
    await generate_liked_songs(uid)

async def get_auto_playlists(uid: str):
    auto_ref = get_auto_playlists_ref(uid)
    docs = auto_ref.stream()
    return [doc.to_dict() for doc in docs]

async def get_auto_playlist_songs(uid: str, playlist_id: str):
    songs_ref = get_auto_playlist_songs_ref(uid, playlist_id)
    docs = songs_ref.order_by("added_at", direction="DESCENDING").stream()
    return [doc.to_dict() for doc in docs]
