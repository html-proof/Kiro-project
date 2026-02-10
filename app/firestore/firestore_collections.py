from app.firestore.firestore_client import get_firestore_client
from fastapi import HTTPException

def _get_db():
    """Get Firestore client or raise error if unavailable"""
    db = get_firestore_client()
    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Firestore is not available. Firebase credentials not configured."
        )
    return db

def get_user_ref(uid: str):
    return _get_db().collection("users").document(uid)

def get_user_likes_ref(uid: str):
    return _get_db().collection("users").document(uid).collection("likes")

def get_user_history_ref(uid: str):
    return _get_db().collection("users").document(uid).collection("history")

def get_user_playlists_ref(uid: str):
    return _get_db().collection("users").document(uid).collection("playlists")

def get_playlist_songs_ref(uid: str, playlist_id: str):
    return _get_db().collection("users").document(uid).collection("playlists").document(playlist_id).collection("songs")

def get_auto_playlists_ref(uid: str):
    return _get_db().collection("users").document(uid).collection("auto_playlists")

def get_auto_playlist_songs_ref(uid: str, playlist_id: str):
    return _get_db().collection("users").document(uid).collection("auto_playlists").document(playlist_id).collection("songs")
