# Musicly Backend API Documentation

Base URL: `https://your-domain.railway.app`

## Authentication

Most endpoints require Firebase ID token in Authorization header:

```
Authorization: Bearer YOUR_FIREBASE_ID_TOKEN
```

---

## Auth Endpoints

### POST /auth/login

Login with Firebase token and create/get user profile.

**Request:**
```json
{
  "id_token": "firebase_id_token_here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "uid": "user123",
    "email": "user@example.com",
    "name": "John Doe",
    "photo_url": "https://...",
    "selected_languages": [],
    "selected_artists": []
  }
}
```

---

## Music Endpoints

### GET /search?q={query}

Search for music on YouTube with strict filtering.

**Parameters:**
- `q` (required): Search query

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "video_id",
      "title": "Song Title",
      "artist": "Artist Name",
      "thumbnail": "https://...",
      "duration": 240
    }
  ]
}
```

### GET /resolve?id={video_id}&quality={quality}

Resolve audio stream URL for a video.

**Parameters:**
- `id` (required): YouTube video ID
- `quality` (optional): ultra/saver/high (default: saver)

**Response:**
```json
{
  "success": true,
  "data": {
    "stream_url": "https://...",
    "bitrate": 64,
    "format": "m4a"
  }
}
```

### GET /play?id={video_id}&quality={quality}

Stream audio with proxy. Supports Range requests.

**Parameters:**
- `id` (required): YouTube video ID
- `quality` (optional): ultra/saver/high (default: saver)

**Headers:**
- `Range` (optional): bytes=0-1024

**Response:** Audio stream (binary)

### GET /preview?id={video_id}

Stream first 15 seconds or 300KB for preview.

**Parameters:**
- `id` (required): YouTube video ID

**Response:** Audio stream (binary)

### GET /resolve-video?id={video_id}&quality={quality}

Resolve video stream URL.

**Parameters:**
- `id` (required): YouTube video ID
- `quality` (optional): low/medium/high (default: low)

**Response:**
```json
{
  "success": true,
  "data": {
    "stream_url": "https://...",
    "resolution": "360p",
    "format": "mp4"
  }
}
```

### GET /play-video?id={video_id}&quality={quality}

Stream video with proxy. Supports Range requests.

---

## User Endpoints (Require Auth)

### POST /user/preferences

Save user language and artist preferences.

**Request:**
```json
{
  "selected_languages": ["Tamil", "Hindi"],
  "selected_artists": ["Anirudh", "Arijit Singh"]
}
```

### POST /user/play

Track song play in history.

**Request:**
```json
{
  "video_id": "abc123",
  "title": "Song Title",
  "artist": "Artist Name",
  "thumbnail": "https://...",
  "duration": 240,
  "language": "Tamil"
}
```

### POST /user/like

Like a song.

**Request:**
```json
{
  "video_id": "abc123",
  "title": "Song Title",
  "artist": "Artist Name",
  "thumbnail": "https://...",
  "duration": 240,
  "language": "Tamil"
}
```

### POST /user/progress

Save playback progress.

**Request:**
```json
{
  "video_id": "abc123",
  "position": 120,
  "duration": 240
}
```

### GET /user/history

Get user listening history (last 50 songs).

### GET /user/likes

Get all liked songs.

### GET /user/recent

Get recently played songs (last 20).

### GET /user/recommend

Get personalized recommendations based on preferences and history.

---

## Playlist Endpoints (Require Auth)

### POST /playlist/create

Create a new playlist.

**Request:**
```json
{
  "name": "My Playlist",
  "description": "My favorite songs",
  "tags": ["romantic", "chill"]
}
```

### POST /playlist/add-song

Add song to playlist.

**Request:**
```json
{
  "playlist_id": "playlist123",
  "video_id": "abc123",
  "title": "Song Title",
  "artist": "Artist Name",
  "thumbnail": "https://...",
  "duration": 240
}
```

### POST /playlist/remove-song

Remove song from playlist.

**Request:**
```json
{
  "playlist_id": "playlist123",
  "video_id": "abc123"
}
```

### GET /playlist/list

Get all user playlists.

### GET /playlist/{playlist_id}

Get songs in a playlist.

### DELETE /playlist/{playlist_id}

Delete a playlist.

### GET /playlist/auto/list

Get all auto-generated playlists (On Repeat, Daily Mix, etc).

### GET /playlist/auto/{playlist_id}

Get songs in an auto playlist.

### POST /playlist/auto/regenerate

Regenerate all auto playlists based on latest data.

---

## Recommendation Endpoints

### GET /recommend/type?type={type}&language={language}

Get recommendations by mood/type.

**Parameters:**
- `type` (required): romantic/party/chill/workout/sleep/sad/devotional/motivational
- `language` (optional): Language filter (default: English)

### GET /recommend/artist?name={artist}&language={language}

Get songs by artist.

**Parameters:**
- `name` (required): Artist name
- `language` (optional): Language filter

### GET /recommend/similar?id={video_id}

Get similar songs.

### GET /recommend/because-liked

Get recommendations based on liked songs.

---

## Quality Modes

- **ultra**: 48kbps (lowest data usage)
- **saver**: 64kbps (default, balanced)
- **high**: 128kbps+ (best quality)

## Caching Strategy

- Search results: 5 minutes
- Stream URLs: 15-30 minutes
- Recommendations: 2-5 minutes
- Tag/type results: 5 minutes

## Rate Limiting

No rate limiting currently. Consider implementing for production.

## Error Responses

```json
{
  "success": false,
  "message": "Error description",
  "code": 400
}
```

Common status codes:
- 200: Success
- 400: Bad request
- 401: Unauthorized
- 404: Not found
- 500: Server error
