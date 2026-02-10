# Local Development Setup

## Prerequisites

- Python 3.9+
- Redis (local or Docker)
- Firebase project

## Step 1: Install Dependencies

```bash
cd musicly-backend
pip install -r requirements.txt
```

## Step 2: Setup Redis (Docker)

```bash
docker run -d -p 6379:6379 redis:latest
```

Or install Redis locally based on your OS.

## Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Firebase credentials:

```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=http://localhost:3000
APP_ENV=development
```

## Step 4: Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

## Step 5: Test the API

Open browser: `http://localhost:8000/docs`

You'll see the interactive API documentation (Swagger UI).

## Testing Endpoints

### Search Music
```bash
curl "http://localhost:8000/search?q=arijit+singh"
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Common Issues

### Redis Connection Error
- Make sure Redis is running: `redis-cli ping` should return `PONG`

### Firebase Auth Error
- Verify your service account JSON is valid
- Check Firebase project permissions

### yt-dlp Errors
- Update yt-dlp: `pip install -U yt-dlp`
- Some videos may be region-restricted

## Development Tips

- Use `--reload` flag for auto-restart on code changes
- Check logs for debugging
- Use Redis CLI to inspect cache: `redis-cli`
- Monitor Firebase usage in console
