from app.firestore.firestore_collections import get_user_playlists_ref, get_playlist_songs_ref
from app.utils.time_utils import now_timestamp
import uuid

async def create_playlist(uid: str, name: str, description: str = "", tags: list = []):
    playlists_ref = get_user_playlists_ref(uid)
    playlist_id = str(uuid.uuid4())
    
    playlist_data = {
        "playlist_id": playlist_id,
        "name": name,
        "description": description,
        "cover_image": "",
        "tags": tags,
        "created_at": now_timestamp(),
        "updated_at": now_timestamp()
    }
    
    playlists_ref.document(playlist_id).set(playlist_data)
    return playlist_data

async def add_song_to_playlist(uid: str, playlist_id: str, song_data: dict):
    songs_ref = get_playlist_songs_ref(uid, playlist_id)
    video_id = song_data.get("video_id")
    song_data["added_at"] = now_timestamp()
    songs_ref.document(video_id).set(song_data)

async def remove_song_from_playlist(uid: str, playlist_id: str, video_id: str):
    songs_ref = get_playlist_songs_ref(uid, playlist_id)
    songs_ref.document(video_id).delete()

async def get_user_playlists(uid: str):
    playlists_ref = get_user_playlists_ref(uid)
    docs = playlists_ref.order_by("created_at", direction="DESCENDING").stream()
    return [doc.to_dict() for doc in docs]

async def get_playlist_songs(uid: str, playlist_id: str):
    songs_ref = get_playlist_songs_ref(uid, playlist_id)
    docs = songs_ref.order_by("added_at", direction="DESCENDING").stream()
    return [doc.to_dict() for doc in docs]

async def delete_playlist(uid: str, playlist_id: str):
    playlists_ref = get_user_playlists_ref(uid)
    playlists_ref.document(playlist_id).delete()
