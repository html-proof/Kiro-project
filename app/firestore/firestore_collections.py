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
# CLEAN STRUCTURE: users/{userId}/...
# Each user has unique data - no conflicts
# ============================================================================

def get_user_profile_ref(uid: str):
    """Get user profile document (email, name, languages, moods, created_at)"""
    return _get_db().collection("users").document(uid).collection("profile").document("data")

def get_user_playback_ref(uid: str):
    """Get user playback document (current_playing, previous_played, next_recommended)"""
    return _get_db().collection("users").document(uid).collection("playback").document("state")

def get_user_history_collection(uid: str):
    """Get user play history subcollection - {songId} with timestamp"""
    return _get_db().collection("users").document(uid).collection("history")

def get_user_searches_collection(uid: str):
    """Get user search history subcollection - {searchId} with timestamp"""
    return _get_db().collection("users").document(uid).collection("searches")

def get_user_likes_collection(uid: str):
    """Get user likes subcollection - {songId} liked songs"""
    return _get_db().collection("users").document(uid).collection("likes")

# ============================================================================
# LEGACY SUPPORT (for backward compatibility)
# ============================================================================

def get_user_ref(uid: str):
    """Legacy: Get user document reference"""
    return get_user_profile_ref(uid)

def get_user_likes_ref(uid: str):
    """Legacy: Get user likes collection"""
    return get_user_likes_collection(uid)

def get_user_history_ref(uid: str):
    """Legacy: Get user history collection"""
    return get_user_history_collection(uid)

def get_user_playlists_ref(uid: str):
    """Legacy: Playlists (can be added later if needed)"""
    return _get_db().collection("users").document(uid).collection("playlists")

def get_playlist_songs_ref(uid: str, playlist_id: str):
    """Legacy: Playlist songs"""
    return _get_db().collection("users").document(uid).collection("playlists").document(playlist_id).collection("songs")

def get_auto_playlists_ref(uid: str):
    """Legacy: Auto playlists"""
    return get_user_playlists_ref(uid)

def get_auto_playlist_songs_ref(uid: str, playlist_id: str):
    """Legacy: Auto playlist songs"""
    return get_playlist_songs_ref(uid, playlist_id)
