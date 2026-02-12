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

# ============================================================================
# ORGANIZED STRUCTURE: users/{userId}/...
# ============================================================================

def get_user_profile_ref(uid: str):
    """Get user profile document reference"""
    return _get_db().collection("users").document(uid).collection("profile").document("data")

def get_user_preferences_ref(uid: str):
    """Get user preferences document reference"""
    return _get_db().collection("users").document(uid).collection("preferences").document("data")

def get_user_playback_ref(uid: str):
    """Get user playback state document reference"""
    return _get_db().collection("users").document(uid).collection("playback").document("current")

def get_user_history_collection(uid: str):
    """Get user play history collection reference"""
    return _get_db().collection("users").document(uid).collection("history")

def get_user_searches_collection(uid: str):
    """Get user search history collection reference"""
    return _get_db().collection("users").document(uid).collection("searches")

def get_user_likes_collection(uid: str):
    """Get user likes collection reference"""
    return _get_db().collection("users").document(uid).collection("likes")

def get_user_playlists_collection(uid: str):
    """Get user playlists collection reference"""
    return _get_db().collection("users").document(uid).collection("playlists")

def get_playlist_songs_collection(uid: str, playlist_id: str):
    """Get songs in a specific playlist"""
    return _get_db().collection("users").document(uid).collection("playlists").document(playlist_id).collection("songs")

def get_user_recommendations_collection(uid: str):
    """Get user recommendations collection reference"""
    return _get_db().collection("users").document(uid).collection("recommendations")

# ============================================================================
# LEGACY SUPPORT (for backward compatibility)
# ============================================================================

def get_user_ref(uid: str):
    """Legacy: Get user document reference (maps to profile)"""
    return get_user_profile_ref(uid)

def get_user_likes_ref(uid: str):
    """Legacy: Get user likes collection"""
    return get_user_likes_collection(uid)

def get_user_history_ref(uid: str):
    """Legacy: Get user history collection"""
    return get_user_history_collection(uid)

def get_user_playlists_ref(uid: str):
    """Legacy: Get user playlists collection"""
    return get_user_playlists_collection(uid)

def get_playlist_songs_ref(uid: str, playlist_id: str):
    """Legacy: Get playlist songs collection"""
    return get_playlist_songs_collection(uid, playlist_id)

def get_auto_playlists_ref(uid: str):
    """Legacy: Auto playlists (deprecated, use regular playlists)"""
    return get_user_playlists_collection(uid)

def get_auto_playlist_songs_ref(uid: str, playlist_id: str):
    """Legacy: Auto playlist songs (deprecated, use regular playlist songs)"""
    return get_playlist_songs_collection(uid, playlist_id)
