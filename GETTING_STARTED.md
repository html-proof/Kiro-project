# 🎵 Getting Started with Musicly Backend

Welcome! This guide will help you get started with the Musicly Backend project.

---

## 📚 Documentation Overview

We've created comprehensive documentation for you:

### Quick Start
- **QUICKSTART.md** - Get running in 5 minutes
- **LOCAL_SETUP.md** - Detailed local development setup

### Deployment
- **DEPLOYMENT.md** - Railway.com deployment guide
- **DEPLOYMENT_CHECKLIST.md** - Pre-launch checklist

### Reference
- **API_DOCUMENTATION.md** - Complete API reference
- **FEATURES.md** - All 150+ features explained
- **PROJECT_SUMMARY.md** - Architecture overview

### Help
- **TROUBLESHOOTING.md** - Common issues and solutions
- **README.md** - Project overview

---

## 🚀 Choose Your Path

### Path 1: Quick Test (5 minutes)
Perfect for: Trying out the API quickly

1. Read **QUICKSTART.md**
2. Follow the 5 steps
3. Test at http://localhost:8000/docs

### Path 2: Local Development (15 minutes)
Perfect for: Development and testing

1. Read **LOCAL_SETUP.md**
2. Set up Redis and Firebase
3. Configure environment
4. Start developing

### Path 3: Production Deployment (30 minutes)
Perfect for: Deploying to production

1. Read **DEPLOYMENT.md**
2. Follow **DEPLOYMENT_CHECKLIST.md**
3. Deploy to Railway
4. Test in production

---

## 📖 Recommended Reading Order

### For Developers
1. **README.md** - Understand what this is
2. **QUICKSTART.md** - Get it running
3. **API_DOCUMENTATION.md** - Learn the endpoints
4. **FEATURES.md** - Explore capabilities
5. **TROUBLESHOOTING.md** - When things go wrong

### For DevOps/Deployment
1. **README.md** - Project overview
2. **LOCAL_SETUP.md** - Test locally first
3. **DEPLOYMENT.md** - Deploy to Railway
4. **DEPLOYMENT_CHECKLIST.md** - Ensure nothing is missed
5. **TROUBLESHOOTING.md** - Fix issues

### For Frontend Developers
1. **README.md** - What the backend does
2. **API_DOCUMENTATION.md** - How to use the API
3. **FEATURES.md** - What features are available
4. **QUICKSTART.md** - Run backend locally for testing

### For Project Managers
1. **README.md** - Project overview
2. **FEATURES.md** - Complete feature list
3. **PROJECT_SUMMARY.md** - Technical architecture
4. **DEPLOYMENT_CHECKLIST.md** - Launch requirements

---

## 🎯 Key Concepts

### Architecture
```
Flutter App → FastAPI Backend → YouTube (via yt-dlp)
                ↓
            Firebase (Auth + Firestore)
                ↓
            Redis (Caching)
```

### Data Flow
1. User searches for music
2. Backend searches YouTube with filters
3. Results cached in Redis
4. User plays song
5. Backend extracts audio stream
6. Stream URL cached
7. Backend proxies stream to app
8. Play tracked in Firestore

### Key Features
- 🔐 Firebase Authentication
- 🎵 YouTube music search
- 🎧 Audio/video streaming
- 📊 Smart recommendations
- 📁 Playlists (manual + auto)
- 💾 Redis caching
- 🗄️ Firestore database

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** Firebase Firestore
- **Cache:** Redis
- **Auth:** Firebase Admin SDK
- **YouTube:** yt-dlp
- **Deployment:** Railway.com

---

## 📋 Prerequisites

Before you start, you need:

1. **Python 3.9+**
   ```bash
   python --version
   ```

2. **Redis**
   ```bash
   # Docker (easiest)
   docker run -d -p 6379:6379 redis:latest
   ```

3. **Firebase Project**
   - Create at https://console.firebase.google.com
   - Enable Authentication
   - Enable Firestore
   - Generate service account key

4. **Git** (for deployment)
   ```bash
   git --version
   ```

---

## 🎬 Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Redis
docker run -d -p 6379:6379 redis:latest

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run server
uvicorn app.main:app --reload

# 5. Test
curl http://localhost:8000/health
```

---

## 🧪 Testing the API

### Option 1: Interactive Docs (Recommended)
Open browser: http://localhost:8000/docs

### Option 2: Command Line
```bash
# Health check
curl http://localhost:8000/health

# Search music
curl "http://localhost:8000/search?q=arijit+singh"

# Run test script
python test_api.py
```

### Option 3: Postman/Thunder Client
Import the API endpoints from the docs page.

---

## 📱 Frontend Integration

### Get API URL
- **Local:** http://localhost:8000
- **Production:** https://your-app.railway.app

### Authentication Flow
1. User logs in with Firebase (frontend)
2. Get Firebase ID token
3. Send token in Authorization header:
   ```
   Authorization: Bearer YOUR_TOKEN
   ```

### Example: Search Music
```dart
// Flutter example
final response = await http.get(
  Uri.parse('$baseUrl/search?q=arijit singh'),
);
```

### Example: Play Music
```dart
// Flutter example
final player = AudioPlayer();
await player.play(UrlSource('$baseUrl/play?id=$videoId&quality=saver'));
```

---

## 🔧 Development Workflow

### 1. Make Changes
Edit files in `app/` directory

### 2. Test Locally
```bash
uvicorn app.main:app --reload
```

### 3. Test Endpoints
Use http://localhost:8000/docs

### 4. Commit Changes
```bash
git add .
git commit -m "Your message"
git push
```

### 5. Deploy
Railway auto-deploys on push (if connected)

---

## 🐛 Common Issues

### "Connection refused"
→ Redis not running. Start Redis.

### "Firebase error"
→ Check service account JSON in .env

### "Module not found"
→ Run `pip install -r requirements.txt`

### "Port in use"
→ Use different port: `--port 8001`

**More solutions:** See TROUBLESHOOTING.md

---

## 📊 Project Structure

```
musicly-backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── firebase/            # Auth & init
│   ├── firestore/           # Database
│   ├── redis/               # Caching
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   └── utils/               # Helpers
├── requirements.txt         # Dependencies
├── Procfile                 # Railway config
├── .env.example             # Environment template
└── [Documentation files]
```

---

## 🎓 Learning Resources

### FastAPI
- Official docs: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### Firebase
- Console: https://console.firebase.google.com
- Docs: https://firebase.google.com/docs

### Redis
- Try it: https://try.redis.io
- Docs: https://redis.io/docs

### yt-dlp
- GitHub: https://github.com/yt-dlp/yt-dlp
- Usage: https://github.com/yt-dlp/yt-dlp#usage

---

## 🚀 Next Steps

### After Setup
1. ✅ Test all endpoints
2. ✅ Integrate with frontend
3. ✅ Test authentication flow
4. ✅ Test music playback
5. ✅ Deploy to Railway

### Before Production
1. ✅ Complete DEPLOYMENT_CHECKLIST.md
2. ✅ Set up monitoring
3. ✅ Configure Firebase security rules
4. ✅ Test under load
5. ✅ Set up backups

### Ongoing
1. 📊 Monitor usage
2. 🔄 Update yt-dlp regularly
3. 🐛 Fix bugs
4. ✨ Add features
5. 📈 Optimize performance

---

## 💡 Pro Tips

1. **Use --reload during development**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Check Redis cache**
   ```bash
   redis-cli
   > KEYS *
   > GET search:arijit
   ```

3. **Monitor Firebase usage**
   - Check Firebase Console daily
   - Set up billing alerts

4. **Keep yt-dlp updated**
   ```bash
   pip install -U yt-dlp
   ```

5. **Use interactive docs**
   - http://localhost:8000/docs
   - Test endpoints directly

---

## 🤝 Getting Help

### Documentation
- Check relevant .md file first
- TROUBLESHOOTING.md for common issues

### Community
- GitHub Issues (if public repo)
- Team chat/Slack

### Support
- Railway: https://railway.app/help
- Firebase: https://firebase.google.com/support

---

## ✅ Success Checklist

Before you start coding:
- [ ] Read README.md
- [ ] Complete QUICKSTART.md
- [ ] API running locally
- [ ] Can search music
- [ ] Can play audio
- [ ] Understand authentication

Before deployment:
- [ ] Tested all features locally
- [ ] Firebase configured
- [ ] Redis working
- [ ] Environment variables ready
- [ ] Read DEPLOYMENT.md

After deployment:
- [ ] All endpoints working
- [ ] Authentication working
- [ ] Music playback working
- [ ] Monitoring set up
- [ ] Team notified

---

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Run the backend locally
- ✅ Understand the API
- ✅ Deploy to production
- ✅ Integrate with frontend
- ✅ Troubleshoot issues

**Start with QUICKSTART.md and you'll be running in 5 minutes!**

---

**Questions?** Check the documentation files or reach out to the team.

**Happy Coding! 🎵**
