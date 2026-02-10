from app.firestore.firestore_collections import get_user_likes_ref
from app.utils.time_utils import now_timestamp

async def add_like(uid: str, song_data: dict):
    likes_ref = get_user_likes_ref(uid)
    video_id = song_data.get("video_id")
    song_data["liked_at"] = now_timestamp()
    likes_ref.document(video_id).set(song_data)

async def get_user_likes(uid: str):
    likes_ref = get_user_likes_ref(uid)
    docs = likes_ref.order_by("liked_at", direction="DESCENDING").stream()
    return [doc.to_dict() for doc in docs]

async def remove_like(uid: str, video_id: str):
    likes_ref = get_user_likes_ref(uid)
    likes_ref.document(video_id).delete()
