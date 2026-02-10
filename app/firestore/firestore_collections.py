from app.firestore.firestore_client import db

def get_user_ref(uid: str):
    return db.collection("users").document(uid)

def get_user_likes_ref(uid: str):
    return db.collection("users").document(uid).collection("likes")

def get_user_history_ref(uid: str):
    return db.collection("users").document(uid).collection("history")

def get_user_playlists_ref(uid: str):
    return db.collection("users").document(uid).collection("playlists")

def get_playlist_songs_ref(uid: str, playlist_id: str):
    return db.collection("users").document(uid).collection("playlists").document(playlist_id).collection("songs")

def get_auto_playlists_ref(uid: str):
    return db.collection("users").document(uid).collection("auto_playlists")

def get_auto_playlist_songs_ref(uid: str, playlist_id: str):
    return db.collection("users").document(uid).collection("auto_playlists").document(playlist_id).collection("songs")
