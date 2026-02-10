# Musicly Backend - Project Summary

## Overview

Production-ready FastAPI backend for a Spotify-like music streaming application with YouTube as the content source.

## Key Features Implemented

### 1. Authentication & User Management
- Firebase Authentication (Google + Email)
- User profile creation and management
- Token-based authorization for protected endpoints

### 2. Music Search & Streaming
- YouTube search with strict content filtering
- Audio-only streaming (no downloads)
- Video streaming support
- Quality selector (ultra 48kbps / saver 64kbps / high 128kbps)
- Preview mode (300KB data saver)
- HTTP Range request support for seeking

### 3. Content Filtering
Strict filtering to include ONLY:
- Songs
- Official audio
- Music videos
- Podcasts

Filters OUT:
- News, politics, interviews, speeches
- Shorts, reels, memes
- Movie content, trailers
- Remixes, 8D, slowed versions
- Live streams
- Videos <60s or >12min

### 4. User Features
- Listening history tracking
- Like/favorite songs
- Playback progress saving
- Language and artist preferences
- Continue listening from last position

### 5. Playlists
**Manual Playlists:**
- Create custom playlists
- Add/remove songs
- Tag-based organization

**Auto Playlists:**
- On Repeat (top 30 most played in 30 days)
- Daily Mix (personalized mix)
- Recently Played (last 50 songs)
- Liked Songs (all favorites)

### 6. Recommendation System
- Personalized recommendations based on:
  - Selected languages (+40 score)
  - Selected artists (+50 score)
  - Listening history (+25 score)
  - Liked songs (+100 score)
  - Recently played penalty (-80 score)

- Tag/mood recommendations:
  - romantic, party, chill, workout, sleep, sad, devotional, motivational

- Artist radio
- Similar songs
- "Because you liked" suggestions

### 7. Caching Strategy (Redis)
- Search results: 300s TTL
- Audio streams: 900s TTL
- Video streams: 900s TTL
- Recommendations: 300s TTL
- Tag/type results: 300s TTL

### 8. Database (Firestore)
Collections structure:
```
users/{uid}
  ├── likes/{video_id}
  ├── history/{auto_id}
  ├── playlists/{playlist_id}
  │   └── songs/{video_id}
  └── auto_playlists/{playlist_id}
      └── songs/{video_id}
```

### 9. Data Efficiency
- Default quality: 64kbps (lower than Spotify)
- Preview-first strategy
- Audio-only by default
- Video only on fast internet
- Efficient caching

## Technology Stack

- **Framework:** FastAPI
- **Database:** Firebase Firestore
- **Cache:** Redis
- **Auth:** Firebase Admin SDK
- **YouTube:** yt-dlp
- **Deployment:** Railway.com

## Project Structure

```
musicly-backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Settings & env vars
│   ├── firebase/               # Firebase auth & init
│   ├── firestore/              # Firestore client & collections
│   ├── redis/                  # Redis client & caching
│   ├── routes/                 # API endpoints
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── music_routes.py
│   │   ├── recommend_routes.py
│   │   └── playlist_routes.py
│   ├── services/               # Business logic
│   │   ├── youtube_search_service.py
│   │   ├── audio_resolver_service.py
│   │   ├── video_resolver_service.py
│   │   ├── proxy_stream_service.py
│   │   ├── proxy_video_stream_service.py
│   │   ├── user_history_service.py
│   │   ├── user_like_service.py
│   │   ├── playlist_service.py
│   │   ├── auto_playlist_service.py
│   │   └── recommendation_service.py
│   └── utils/                  # Helper functions
│       ├── response_utils.py
│       ├── time_utils.py
│       ├── quality_utils.py
│       ├── filter_utils.py
│       └── query_builder_utils.py
├── requirements.txt
├── Procfile                    # Railway deployment
├── .env.example
├── README.md
├── API_DOCUMENTATION.md
├── LOCAL_SETUP.md
├── DEPLOYMENT.md
└── PROJECT_SUMMARY.md
```

## API Endpoints Summary

### Auth
- POST /auth/login

### Music
- GET /search
- GET /resolve
- GET /play
- GET /preview
- GET /resolve-video
- GET /play-video

### User (Protected)
- POST /user/preferences
- POST /user/play
- POST /user/like
- POST /user/progress
- GET /user/history
- GET /user/likes
- GET /user/recent
- GET /user/recommend

### Playlists (Protected)
- POST /playlist/create
- POST /playlist/add-song
- POST /playlist/remove-song
- GET /playlist/list
- GET /playlist/{id}
- DELETE /playlist/{id}
- GET /playlist/auto/list
- GET /playlist/auto/{id}
- POST /playlist/auto/regenerate

### Recommendations
- GET /recommend/type
- GET /recommend/artist
- GET /recommend/similar
- GET /recommend/because-liked

## Security Features

- Firebase token verification on protected routes
- User data isolation (users can only access their own data)
- CORS configuration
- Environment-based configuration
- No sensitive data in code

## Performance Optimizations

- Redis caching for frequently accessed data
- Background pre-resolution of top search results
- Efficient Firestore queries with indexing
- Stream proxying without full download
- Quality-based bitrate selection

## Deployment Ready

- Railway.com compatible
- Environment variable configuration
- Procfile for automatic deployment
- No file-based credentials
- Production-ready error handling

## Next Steps for Production

1. Add rate limiting
2. Implement request logging
3. Add monitoring/alerting
4. Set up CI/CD pipeline
5. Add comprehensive tests
6. Implement analytics
7. Add admin dashboard
8. Optimize caching strategies
9. Add CDN for static assets
10. Implement backup strategies

## Maintenance

- Update yt-dlp regularly: `pip install -U yt-dlp`
- Monitor Redis memory usage
- Check Firestore quotas
- Review Firebase costs
- Update dependencies for security patches

## License

Proprietary - All rights reserved
