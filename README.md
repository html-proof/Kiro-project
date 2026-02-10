# Musicly Backend

Production-ready FastAPI backend for Spotify-like music streaming app.

## Features

- Firebase Authentication (Google + Email)
- Firestore database
- Redis caching
- YouTube search with strict filtering
- Audio/Video streaming proxy
- Smart recommendations
- Auto playlists (On Repeat, Daily Mix, Recently Played, Liked Songs)
- Manual playlists
- Preview mode (300KB data saver)
- Quality selector (ultra/saver/high)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run locally:
```bash
uvicorn app.main:app --reload
```

## Deploy to Railway

1. Push to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy automatically

## API Endpoints

### Auth
- POST /auth/login

### User
- POST /user/preferences
- POST /user/play
- POST /user/like
- POST /user/progress
- GET /user/history
- GET /user/likes
- GET /user/recent
- GET /user/recommend

### Music
- GET /search
- GET /resolve
- GET /play
- GET /preview
- GET /resolve-video
- GET /play-video

### Playlists
- POST /playlist/create
- POST /playlist/add-song
- POST /playlist/remove-song
- GET /playlist/list
- GET /playlist/{playlist_id}
- DELETE /playlist/{playlist_id}
- GET /playlist/auto/list
- GET /playlist/auto/{playlist_id}
- POST /playlist/auto/regenerate

### Recommendations
- GET /recommend/type
- GET /recommend/artist
- GET /recommend/similar
- GET /recommend/because-liked
# Kiro-project
