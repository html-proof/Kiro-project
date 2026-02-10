from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.firebase.firebase_auth import verify_token
from app.services.playlist_service import (
    create_playlist, add_song_to_playlist, remove_song_from_playlist,
    get_user_playlists, get_playlist_songs, delete_playlist
)
from app.services.auto_playlist_service import (
    regenerate_all_auto_playlists, get_auto_playlists, get_auto_playlist_songs
)
from app.utils.response_utils import success_response

router = APIRouter()

class CreatePlaylistRequest(BaseModel):
    name: str
    description: str = ""
    tags: list = []

class AddSongRequest(BaseModel):
    playlist_id: str
    video_id: str
    title: str
    artist: str
    thumbnail: str
    duration: int

class RemoveSongRequest(BaseModel):
    playlist_id: str
    video_id: str

@router.post("/create")
async def create_new_playlist(request: CreatePlaylistRequest, token: dict = Depends(verify_token)):
    uid = token["uid"]
    playlist = await create_playlist(uid, request.name, request.description, request.tags)
    return success_response(playlist, "Playlist created")

@router.post("/add-song")
async def add_song(request: AddSongRequest, token: dict = Depends(verify_token)):
    uid = token["uid"]
    song_data = request.dict()
    playlist_id = song_data.pop("playlist_id")
    await add_song_to_playlist(uid, playlist_id, song_data)
    return success_response({}, "Song added")

@router.post("/remove-song")
async def remove_song(request: RemoveSongRequest, token: dict = Depends(verify_token)):
    uid = token["uid"]
    await remove_song_from_playlist(uid, request.playlist_id, request.video_id)
    return success_response({}, "Song removed")

@router.get("/list")
async def list_playlists(token: dict = Depends(verify_token)):
    uid = token["uid"]
    playlists = await get_user_playlists(uid)
    return success_response(playlists)

@router.get("/{playlist_id}")
async def get_playlist(playlist_id: str, token: dict = Depends(verify_token)):
    uid = token["uid"]
    songs = await get_playlist_songs(uid, playlist_id)
    return success_response(songs)

@router.delete("/{playlist_id}")
async def remove_playlist(playlist_id: str, token: dict = Depends(verify_token)):
    uid = token["uid"]
    await delete_playlist(uid, playlist_id)
    return success_response({}, "Playlist deleted")

@router.get("/auto/list")
async def list_auto_playlists(token: dict = Depends(verify_token)):
    uid = token["uid"]
    playlists = await get_auto_playlists(uid)
    return success_response(playlists)

@router.get("/auto/{playlist_id}")
async def get_auto_playlist(playlist_id: str, token: dict = Depends(verify_token)):
    uid = token["uid"]
    songs = await get_auto_playlist_songs(uid, playlist_id)
    return success_response(songs)

@router.post("/auto/regenerate")
async def regenerate_auto_playlists(token: dict = Depends(verify_token)):
    uid = token["uid"]
    await regenerate_all_auto_playlists(uid)
    return success_response({}, "Auto playlists regenerated")
