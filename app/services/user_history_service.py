from app.firestore.firestore_collections import get_user_history_ref
from app.utils.time_utils import now_timestamp

async def add_to_history(uid: str, song_data: dict):
    history_ref = get_user_history_ref(uid)
    song_data["played_at"] = now_timestamp()
    song_data["updated_at"] = now_timestamp()
    history_ref.add(song_data)

async def get_user_history(uid: str, limit: int = 50):
    history_ref = get_user_history_ref(uid)
    docs = history_ref.order_by("played_at", direction="DESCENDING").limit(limit).stream()
    return [doc.to_dict() for doc in docs]

async def update_progress(uid: str, video_id: str, position: int, duration: int):
    history_ref = get_user_history_ref(uid)
    query = history_ref.where("video_id", "==", video_id).order_by("played_at", direction="DESCENDING").limit(1)
    docs = list(query.stream())
    
    if docs:
        doc = docs[0]
        doc.reference.update({
            "last_position_seconds": position,
            "total_duration": duration,
            "updated_at": now_timestamp()
        })
