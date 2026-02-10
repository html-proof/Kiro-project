# 🚀 Quick Start Guide

Get Musicly Backend running in 5 minutes!

## Prerequisites

- Python 3.9+
- Redis (or Docker)
- Firebase project

## Step 1: Clone & Install (2 min)

```bash
cd musicly-backend
pip install -r requirements.txt
```

## Step 2: Start Redis (1 min)

**Option A - Docker (Recommended):**
```bash
docker run -d -p 6379:6379 redis:latest
```

**Option B - Local Redis:**
```bash
# macOS
brew install redis
redis-server

# Ubuntu
sudo apt install redis-server
sudo systemctl start redis

# Windows
# Download from https://redis.io/download
```

## Step 3: Configure Firebase (1 min)

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project (or use existing)
3. Go to Project Settings → Service Accounts
4. Click "Generate New Private Key"
5. Copy the entire JSON content

## Step 4: Setup Environment (30 sec)

```bash
cp .env.example .env
```

Edit `.env`:
```env
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"your-project",...}
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=http://localhost:3000
APP_ENV=development
```

## Step 5: Run! (30 sec)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Test It!

Open browser: http://localhost:8000/docs

Try this:
```bash
curl "http://localhost:8000/search?q=arijit+singh"
```

## 🎉 You're Done!

Your API is running at: `http://localhost:8000`

## Next Steps

1. **Test the API:** Visit http://localhost:8000/docs for interactive docs
2. **Get Firebase Token:** Use Firebase Auth in your frontend
3. **Test Protected Routes:** Use Authorization header with Bearer token
4. **Deploy:** Follow DEPLOYMENT.md for Railway deployment

## Common Issues

### "Connection refused" error
- Make sure Redis is running: `redis-cli ping` should return `PONG`

### "Firebase error"
- Check your service account JSON is valid
- Verify it's properly formatted in .env

### "Module not found"
- Run: `pip install -r requirements.txt`

### Port already in use
- Change port: `uvicorn app.main:app --port 8001`

## Quick Test Script

```bash
python test_api.py
```

## Need Help?

- Check API_DOCUMENTATION.md for endpoint details
- See LOCAL_SETUP.md for detailed setup
- Review DEPLOYMENT.md for production deployment
- Check PROJECT_SUMMARY.md for architecture overview

## Development Tips

- Use `--reload` flag for auto-restart on code changes
- Check logs in terminal for debugging
- Use Redis CLI to inspect cache: `redis-cli`
- Monitor Firebase usage in console
- Test with Postman or Thunder Client

## Production Deployment

Ready to deploy? Follow these guides:
1. DEPLOYMENT.md - Railway deployment guide
2. DEPLOYMENT_CHECKLIST.md - Pre-launch checklist

---

**Happy Coding! 🎵**
