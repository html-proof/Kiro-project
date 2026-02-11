# Musicly Backend Services - Complete Function Summary

## 📋 Overview
The Musicly backend consists of 16 specialized services providing music streaming, recommendations, device management, and real-time synchronization.

---

## 🎵 Core Music Services

### 1. **YouTube Search Service** (`youtube_search_service.py`)
**Purpose**: Intelligent music search with spam filtering and personalization

**Key Functions**:
- `search_songs(query, limit, user_id)` - Smart search with ranking algorithm
  - Intent detection (language-specific searches)
  - Spam/non-music content filtering using trusted channels
  - Personalization based on user's liked artists
  - Duplicate detection
  - Quality scoring (duration, official channels, view count)
  
- `get_stream_url(video_id)` - Get audio stream URL with 2-hour caching
  - Extracts best audio-only format
  - Caches URLs to reduce API calls
  
- `get_artist_details(channel_id)` - Fetch artist info and top songs
  - Returns artist metadata and song list

**Features**:
- Trusted channels filter integration
- Multi-language support
- View count-based popularity boost
- TF-IDF-based content matching

---

### 2. **Recommendation Service** (`recommendation_service.py`)
**Purpose**: Basic personalized recommendations

**Key Functions**:
- `get_user_recommendations(uid)` - Multi-strategy personalized recommendations
  - Strategy 1: Favorite artists (highest priority)
  - Strategy 2: Similar songs based on liked titles
  - Strategy 3: Language-based recommendations
  - Strategy 4: Trending fallback
  - Returns top 20 ranked results
  
- `get_similar_songs(video_id, uid)` - Find similar songs
  - Uses song title and artist for similarity search
  - Keyword extraction for better matching
  
- `get_recommendations_by_artist(artist_name, language)` - Artist-specific recommendations
  
- `get_because_you_liked_recommendations(uid)` - Based on liked songs
  - Samples 3 random liked songs
  - Finds similar artists and songs

**Caching**: 5-minute Redis cache for all recommendations

---

### 3. **Advanced Recommendation Service** (`advanced_recommendation_service.py`)
**Purpose**: ML-powered hybrid recommendation system

**Key Functions**:
- `get_personalized_recommendations(user_id, limit)` - Hybrid approach
  - ML (ALS) recommendations first
  - Artist-based fallback
  - Trending fill
  - Avoids duplicates from user's likes
  
- `get_daily_mix(user_id)` - Daily personalized mix
  - Based on top artists
  - 12 songs
  
- `get_recent_context(user_id)` - Context-aware recommendations
  - Based on last played song
  - ML content similarity first
  - Keyword search fallback
  
- `get_autoplay_next(user_id, current_song_id)` - Smart autoplay
  - Similarity search for current song
  - Favorite artists fallback
  - Avoids recently played songs
  
- `get_similar_songs(song_id, user_id)` - ML-based similarity
  - Content-based filtering
  - Search-based fallback
  
- `get_artist_radio(artist_name, user_id)` - Artist radio station
  - Top songs from artist
  - Official audio prioritized

---

### 4. **ML Recommender Service** (`ml_recommender_service.py`)
**Purpose**: Machine learning models for recommendations

**Key Components**:

**InteractionProcessor**:
- Builds user-item interaction matrix
- Weighting scheme:
  - Complete play: +3
  - Partial play: +1
  - Like: +5
  - Skip: -3

**MLRecommender**:
- `train_als_model()` - Train collaborative filtering model
  - Uses Alternating Least Squares (ALS)
  - 50 factors, 20 iterations
  - Saves model to disk
  
- `get_als_recommendations(user_id, n)` - Collaborative filtering
  - Returns personalized song IDs
  - Based on user-item interactions
  
- `get_content_similarity(song_id, n)` - Content-based similarity
  - Uses TF-IDF on title + artist
  - Cosine similarity calculation
  
- `get_hybrid_recommendations(user_id, seed_song_id, n)` - Combined approach
  - ALS + content-based
  - Removes duplicates

**Features**:
- Model persistence (pickle)
- Metadata retrieval for enrichment
- Sparse matrix optimization

---

## 👤 User Data Services

### 5. **User History Service** (`user_history_service.py`)
**Purpose**: Track user's listening history

**Key Functions**:
- `add_to_history(uid, song_data)` - Add song to history
  - Timestamps: played_at, updated_at
  
- `get_user_history(uid, limit)` - Get recent history
  - Ordered by played_at (descending)
  - Default limit: 50
  
- `update_progress(uid, video_id, position, duration)` - Save playback progress
  - Updates last_position_seconds
  - Tracks total_duration

---

### 6. **User Like Service** (`user_like_service.py`)
**Purpose**: Manage user's liked songs

**Key Functions**:
- `add_like(uid, song_data)` - Like a song
  - Stores with liked_at timestamp
  - Uses video_id as document ID
  
- `get_user_likes(uid)` - Get all liked songs
  - Ordered by liked_at (descending)
  
- `remove_like(uid, video_id)` - Unlike a song
  - Deletes from Firestore

---

### 7. **Playlist Service** (`playlist_service.py`)
**Purpose**: User-created playlist management

**Key Functions**:
- `create_playlist(uid, name, description, tags)` - Create new playlist
  - Generates UUID for playlist_id
  - Stores metadata (name, description, tags, cover_image)
  
- `add_song_to_playlist(uid, playlist_id, song_data)` - Add song
  - Timestamps with added_at
  
- `remove_song_from_playlist(uid, playlist_id, video_id)` - Remove song
  
- `get_user_playlists(uid)` - List all playlists
  - Ordered by created_at
  
- `get_playlist_songs(uid, playlist_id)` - Get playlist songs
  - Ordered by added_at
  
- `delete_playlist(uid, playlist_id)` - Delete playlist

---

### 8. **Auto Playlist Service** (`auto_playlist_service.py`)
**Purpose**: Automatically generated playlists

**Key Functions**:
- `generate_on_repeat(uid)` - Most played songs (last 30 days)
  - Top 30 songs by play count
  - Includes score (play count)
  
- `generate_daily_mix(uid)` - Personalized daily mix
  - Mix of favorites and trending
  
- `generate_recently_played(uid)` - Recent history playlist
  - Last 50 played songs
  
- `generate_liked_songs(uid)` - All liked songs playlist
  - Ordered by liked_at
  
- `regenerate_all_auto_playlists(uid)` - Regenerate all auto playlists
  - Runs all generators
  
- `get_auto_playlists(uid)` - List auto playlists
  
- `get_auto_playlist_songs(uid, playlist_id)` - Get auto playlist songs

**Auto Playlist Types**:
- `on_repeat` - Most played
- `daily_mix` - Personalized mix
- `recently_played` - Recent history
- `liked_songs` - All likes

---

## 🔄 Multi-Device & Sync Services

### 9. **Device Manager Service** (`device_manager_service.py`)
**Purpose**: Multi-device management and active device control

**Key Functions**:
- `register_device(user_id, device_id, device_info)` - Register new device
  - Stores: name, platform, userAgent, lastSeen, isOnline
  - Auto-sets as active if first device
  
- `set_active_device(user_id, device_id)` - Set active playback device
  - Only active device can control playback
  
- `get_active_device(user_id)` - Get current active device ID
  
- `update_device_heartbeat(user_id, device_id)` - Keep device alive
  - Updates lastSeen timestamp
  
- `get_user_devices(user_id)` - List all user devices
  - Includes online status (5-minute timeout)
  
- `cleanup_stale_devices(user_id)` - Remove inactive devices
  - Removes devices not seen in >5 minutes
  
- `validate_device_control(user_id, device_id)` - Check control permission
  - Returns true only if device is active
  
- `remove_device(user_id, device_id)` - Unregister device
  - Auto-switches active device if needed
  
- `get_device_info(user_id, device_id)` - Get device details
  - Includes online status and active status

**Features**:
- 5-minute device timeout
- Automatic active device switching
- Heartbeat monitoring
- Firebase Realtime Database integration

---

### 10. **Network Monitor Service** (`network_monitor_service.py`)
**Purpose**: Network speed monitoring and adaptive quality

**NetworkMonitor Functions**:
- `update_network_speed(user_id, device_id, speed_mbps, latency_ms)` - Update speed
  - Stores speed and latency
  - Calculates recommended quality
  - 5-minute in-memory cache
  
- `get_recommended_quality(speed_mbps)` - Quality recommendation
  - Ultra: ≥2.0 Mbps (320kbps)
  - High: ≥1.0 Mbps (192kbps)
  - Medium: ≥0.5 Mbps (128kbps)
  - Saver: <0.5 Mbps (64kbps)
  
- `get_network_info(user_id, device_id)` - Get network metrics
  - Returns speed, latency, recommended quality
  - Uses cache if available
  
- `get_adaptive_quality(user_id, device_id, requested_quality)` - Adaptive quality
  - Balances user preference with network capability
  - Uses lower of requested vs recommended
  
- `update_connection_type(user_id, device_id, connection_type)` - Track connection
  - wifi, cellular, ethernet, etc.

**AudioOutputMonitor Functions**:
- `update_audio_output(user_id, device_id, output_info)` - Update output device
  - Types: headphones, speaker, bluetooth, external
  - Stores name and isDefault flag
  
- `get_audio_output(user_id, device_id)` - Get current output
  
- `handle_output_change(user_id, device_id, old_output, new_output)` - Handle changes
  - Headphones disconnected → pause playback
  - Headphones connected → show notification
  - Bluetooth connected → show notification
  - Returns action recommendations

**Features**:
- Adaptive bitrate selection
- Connection type tracking
- Audio output device monitoring
- Smart pause on headphone disconnect

---

### 11. **Sync Service** (`sync_service.py`)
**Purpose**: Real-time WebSocket synchronization

**Key Functions**:
- `connect(websocket, user_id, device_id)` - Connect WebSocket
  - Accepts connection
  - Adds to user's room
  - Registers device
  
- `disconnect(websocket, user_id, device_id)` - Disconnect WebSocket
  - Removes from room
  - Unregisters device
  
- `broadcast_to_user(user_id, message, sender)` - Broadcast message
  - Sends to all user's devices except sender
  
- `handle_playback_update(user_id, device_id, state, sender)` - Update playback
  - Validates device control permission
  - Updates Firebase playback state
  - Broadcasts to other devices
  - Rejects if not active device
  
- `handle_device_switch(user_id, new_device_id)` - Switch active device
  - Updates active device
  - Broadcasts switch event
  
- `broadcast_device_switch(user_id, new_active_device_id)` - Notify switch
  - Sends device_switched message
  
- `get_active_device(user_id)` - Get active device
  
- `get_user_devices(user_id)` - List devices

**Message Types**:
- `playback_state_update` - Playback state changed
- `playback_controlled_elsewhere` - Control rejected
- `device_switched` - Active device changed

**Features**:
- Room-based WebSocket management
- Device control validation
- Real-time state synchronization
- Multi-device support

---

## 🎧 Streaming Services

### 12. **Audio Resolver Service** (`audio_resolver_service.py`)
**Purpose**: Resolve audio streams with quality selection

**Key Functions**:
- `resolve_audio_stream(video_id, quality)` - Get audio stream URL
  - Quality options: ultra, high, medium, saver
  - Selects best audio format for target bitrate
  - 15-minute Redis cache
  - Returns: stream_url, bitrate, format

**Features**:
- Quality-based bitrate selection
- Audio-only format extraction
- Stream URL caching

---

### 13. **Video Resolver Service** (`video_resolver_service.py`)
**Purpose**: Resolve video streams

**Key Functions**:
- `resolve_video_stream(video_id, quality)` - Get video stream URL
  - Quality options: low, medium, high
  - Selects best video format
  - 15-minute Redis cache
  - Returns: stream_url, resolution, format

---

### 14. **Proxy Stream Service** (`proxy_stream_service.py`)
**Purpose**: Proxy audio streams through backend

**Key Functions**:
- `proxy_audio_stream(stream_url, range_header)` - Proxy audio
  - Supports range requests (seeking)
  - Streams audio through backend
  - Handles Content-Range headers
  - Returns StreamingResponse

**Features**:
- Range request support
- Proper headers (Content-Type, Accept-Ranges)
- 30-second timeout

---

### 15. **Proxy Video Stream Service** (`proxy_video_stream_service.py`)
**Purpose**: Proxy video streams through backend

**Key Functions**:
- `proxy_video_stream(stream_url, range_header)` - Proxy video
  - Supports range requests
  - Streams video through backend
  - Returns StreamingResponse

---

## 📊 Summary Statistics

### Service Categories:
- **Music Discovery**: 4 services (Search, Recommendations, Advanced Rec, ML)
- **User Data**: 4 services (History, Likes, Playlists, Auto Playlists)
- **Multi-Device**: 3 services (Device Manager, Network Monitor, Sync)
- **Streaming**: 4 services (Audio Resolver, Video Resolver, Audio Proxy, Video Proxy)

### Total Functions: 80+

### Key Technologies:
- **YouTube**: yt-dlp for search and stream extraction
- **ML**: implicit (ALS), scikit-learn (TF-IDF, cosine similarity)
- **Database**: Firebase Firestore, Firebase Realtime Database
- **Cache**: Redis (5-15 minute TTL)
- **Real-time**: WebSocket (FastAPI)
- **Streaming**: httpx, StreamingResponse

### Performance Features:
- Multi-level caching (Redis + in-memory)
- Sparse matrix optimization for ML
- Efficient duplicate detection
- Lazy loading and pagination
- Stream URL caching (2-hour TTL)

### Quality Features:
- Spam/non-music filtering (trusted channels)
- Multi-strategy recommendations
- Adaptive bitrate selection
- Network-aware quality
- Device control validation

---

## 🔗 Service Dependencies

```
YouTube Search ← Recommendation ← Advanced Recommendation ← ML Recommender
                      ↓                      ↓
                User History          User Likes
                      ↓                      ↓
                Auto Playlists ← Playlist Service
                
Device Manager ← Sync Service → Network Monitor
                      ↓
                Audio/Video Resolvers → Proxy Services
```

---

## 🚀 Deployment Status

- **Backend**: Deployed on Railway
- **Repository**: https://github.com/html-proof/Kiro-project.git
- **Branch**: main
- **Latest Commit**: e9daeee (version 1.0.1)
- **Status**: ✅ Running with all services operational

---

## 📝 Notes

- All services use async/await for non-blocking I/O
- Firebase credentials loaded from environment variable
- Redis optional (graceful degradation)
- Comprehensive error handling and logging
- RESTful API + WebSocket support
- CORS enabled for all origins (development mode)
