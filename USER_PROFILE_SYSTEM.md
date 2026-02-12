# 🎯 User Profile System - Complete Implementation

## Overview

Comprehensive user profile and tracking system that stores all user data in Firebase Realtime Database for personalized recommendations and seamless user experience.

## Firebase Realtime Database Structure

```
users/
  └── {user_id}/
      ├── preferences/
      │   ├── languages: ["English", "Hindi", "Tamil"]
      │   ├── moods: ["Happy", "Energetic", "Chill"]
      │   └── updated_at: "2024-01-15T10:30:00Z"
      │
      ├── search_history/
      │   └── {search_id}/
      │       ├── query: "romantic songs"
      │       ├── results_count: 10
      │       └── timestamp: "2024-01-15T10:30:00Z"
      │
      ├── play_history/
      │   └── {play_id}/
      │       ├── song_id: "VIDEO_ID"
      │       ├── title: "Song Title"
      │       ├── artist: "Artist Name"
      │       ├── duration: 180
      │       ├── thumbnail: "https://..."
      │       └── timestamp: "2024-01-15T10:30:00Z"
      │
      ├── song_stats/
      │   └── {song_id}/
      │       ├── play_count: 15
      │       ├── last_played: "2024-01-15T10:30:00Z"
      │       ├── title: "Song Title"
      │       └── artist: "Artist Name"
      │
      ├── playback_positions/
      │   └── {song_id}/
      │       ├── position_ms: 45000
      │       ├── duration_ms: 180000
      │       ├── percentage: 25.0
      │       └── updated_at: "2024-01-15T10:30:00Z"
      │
      └── offline_songs/
          └── {song_id}/
              ├── song_id: "VIDEO_ID"
              ├── title: "Song Title"
              ├── artist: "Artist Name"
              ├── duration: 180
              ├── thumbnail: "https://..."
              ├── file_path: "/storage/music/song.mp3"
              ├── file_size: 1048576
              ├── quality: "ultra"
              └── downloaded_at: "2024-01-15T10:30:00Z"
```

## API Endpoints

### 1. User Preferences (Asked Once on Login)

#### Set Preferences
```http
POST /profile/preferences?user_id=USER123
Content-Type: application/json

{
  "languages": ["English", "Hindi", "Tamil"],
  "moods": ["Happy", "Energetic", "Chill", "Romantic"]
}
```

#### Get Preferences
```http
GET /profile/preferences?user_id=USER123
```

### 2. Search Tracking

#### Track Search
```http
POST /profile/track/search?user_id=USER123
Content-Type: application/json

{
  "query": "romantic songs",
  "results_count": 10
}
```

#### Get Search History
```http
GET /profile/search-history?user_id=USER123&limit=50
```

### 3. Play Tracking

#### Track Play
```http
POST /profile/track/play?user_id=USER123
Content-Type: application/json

{
  "id": "VIDEO_ID",
  "title": "Song Title",
  "artist": "Artist Name",
  "duration": 180,
  "thumbnail": "https://..."
}
```

#### Get Play History
```http
GET /profile/play-history?user_id=USER123&limit=100
```

### 4. Playback Position (Resume Feature)

#### Save Position (When User Pauses)
```http
POST /profile/playback/position?user_id=USER123
Content-Type: application/json

{
  "song_id": "VIDEO_ID",
  "position_ms": 45000,
  "duration_ms": 180000
}
```

#### Get Position (When User Returns)
```http
GET /profile/playback/position?user_id=USER123&song_id=VIDEO_ID
```

Response:
```json
{
  "success": true,
  "data": {
    "position_ms": 45000,
    "duration_ms": 180000,
    "percentage": 25.0,
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Clear Position (When Song Completes)
```http
DELETE /profile/playback/position?user_id=USER123&song_id=VIDEO_ID
```

### 5. Offline Downloads

#### Add Offline Song
```http
POST /profile/offline/add?user_id=USER123
Content-Type: application/json

{
  "song_data": {
    "id": "VIDEO_ID",
    "title": "Song Title",
    "artist": "Artist Name",
    "duration": 180,
    "thumbnail": "https://...",
    "quality": "ultra"
  },
  "file_path": "/storage/music/song.mp3",
  "file_size": 1048576
}
```

#### Get Offline Songs
```http
GET /profile/offline/list?user_id=USER123
```

#### Remove Offline Song
```http
DELETE /profile/offline/remove?user_id=USER123&song_id=VIDEO_ID
```

### 6. User Statistics

#### Get Comprehensive Stats
```http
GET /profile/stats?user_id=USER123
```

Response:
```json
{
  "success": true,
  "data": {
    "user_id": "USER123",
    "preferences": {
      "languages": ["English", "Hindi"],
      "moods": ["Happy", "Energetic"]
    },
    "statistics": {
      "total_plays": 150,
      "total_searches": 45,
      "total_offline": 12,
      "unique_songs_played": 75
    },
    "top_songs": [
      {
        "song_id": "VIDEO_ID",
        "title": "Song Title",
        "artist": "Artist Name",
        "play_count": 15,
        "last_played": "2024-01-15T10:30:00Z"
      }
    ],
    "recent_searches": ["romantic songs", "happy songs"]
  }
}
```

#### Get Recommendation Data
```http
GET /profile/recommendation-data?user_id=USER123
```

Response:
```json
{
  "success": true,
  "data": {
    "user_id": "USER123",
    "languages": ["English", "Hindi"],
    "moods": ["Happy", "Energetic"],
    "top_songs": [...],
    "recent_searches": [...],
    "total_plays": 150
  }
}
```

## Personalized Recommendations

The recommendation system now uses user profile data:

### Enhanced Recommendation Endpoints

#### Get Personalized Recommendations
```http
GET /recommend/for-you?uid=USER123
```

Now returns recommendations based on:
- User's language preferences
- User's mood preferences
- Top played songs
- Recent searches
- Play history

#### Get "Because You Liked" Recommendations
```http
GET /recommend/because-you-liked?uid=USER123
```

Returns songs similar to user's top played songs.

#### Get Mood-Based Recommendations
```http
GET /recommend/mood?uid=USER123&mood=Happy
```

Returns songs matching the mood in user's preferred language.

## User Flow

### 1. First Login (Onboarding)
```
User logs in
    ↓
Show language selection
    ↓
Show mood selection
    ↓
POST /profile/preferences
    ↓
Save to Firebase Realtime Database
```

### 2. Search and Play
```
User searches "romantic songs"
    ↓
POST /profile/track/search
    ↓
User taps song
    ↓
POST /profile/track/play
    ↓
Song plays
```

### 3. Pause and Resume
```
User pauses at 45 seconds
    ↓
POST /profile/playback/position
    (position_ms: 45000)
    ↓
User closes app
    ↓
User returns later
    ↓
GET /profile/playback/position
    ↓
Resume from 45 seconds
```

### 4. Offline Download
```
User downloads song
    ↓
POST /profile/offline/add
    ↓
Song available offline
    ↓
User deletes song
    ↓
DELETE /profile/offline/remove
```

### 5. Personalized Recommendations
```
User opens "For You" tab
    ↓
GET /recommend/for-you?uid=USER123
    ↓
Backend fetches user profile
    ↓
Generates personalized query:
    "{language} {mood} songs like {top_song}"
    ↓
Returns unique recommendations
```

## Benefits

### For Users:
- ✅ Personalized recommendations based on preferences
- ✅ Resume playback from where they left off
- ✅ Track offline downloads
- ✅ See play history and statistics
- ✅ Unique experience per user

### For Recommendations:
- ✅ Language-based filtering
- ✅ Mood-based suggestions
- ✅ Play history analysis
- ✅ Search pattern recognition
- ✅ Top songs similarity

### For Analytics:
- ✅ User engagement metrics
- ✅ Popular songs per user
- ✅ Search trends
- ✅ Playback patterns
- ✅ Offline usage stats

## Firebase Realtime Database URL

```
https://sample-music-65323-default-rtdb.asia-southeast1.firebasedatabase.app/
```

All user data is stored under:
```
/users/{user_id}/
```

## Security Rules (Recommended)

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    }
  }
}
```

## Implementation Status

✅ User profile service created  
✅ Profile API routes created  
✅ Recommendation service enhanced  
✅ Firebase Realtime Database integration  
✅ All endpoints documented  
✅ Ready to deploy  

## Testing

### Test User Preferences
```bash
curl -X POST "https://your-backend.railway.app/profile/preferences?user_id=TEST123" \
  -H "Content-Type: application/json" \
  -d '{"languages": ["English", "Hindi"], "moods": ["Happy", "Energetic"]}'
```

### Test Play Tracking
```bash
curl -X POST "https://your-backend.railway.app/profile/track/play?user_id=TEST123" \
  -H "Content-Type: application/json" \
  -d '{"id": "VIDEO_ID", "title": "Test Song", "artist": "Test Artist", "duration": 180}'
```

### Test Resume Position
```bash
# Save position
curl -X POST "https://your-backend.railway.app/profile/playback/position?user_id=TEST123" \
  -H "Content-Type: application/json" \
  -d '{"song_id": "VIDEO_ID", "position_ms": 45000, "duration_ms": 180000}'

# Get position
curl "https://your-backend.railway.app/profile/playback/position?user_id=TEST123&song_id=VIDEO_ID"
```

### Test Personalized Recommendations
```bash
curl "https://your-backend.railway.app/recommend/for-you?uid=TEST123"
```

## Next Steps

1. Deploy to Railway
2. Test all endpoints
3. Integrate with Flutter app
4. Monitor Firebase Realtime Database
5. Analyze user patterns

---

**Result: Complete user profile system with personalized recommendations, resume playback, offline tracking, and comprehensive analytics!** 🎯🔥
