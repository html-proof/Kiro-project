# 🚂 Railway.com Deployment Guide

Complete step-by-step guide to deploy Musicly Backend to Railway.

---

## ✅ Prerequisites

- [x] GitHub repository: https://github.com/html-proof/Kiro-project
- [x] Railway account (sign up at https://railway.app)
- [x] Firebase service account JSON
- [x] Code pushed to GitHub

---

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Sign Up / Login to Railway

1. Go to: https://railway.app
2. Click "Login" or "Start a New Project"
3. Sign in with GitHub

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: **html-proof/Kiro-project**
4. Railway will auto-detect your project

### Step 3: Add Redis Database

1. In your project, click "New"
2. Select "Database"
3. Choose "Redis"
4. Railway will create Redis and set `REDIS_URL` automatically

### Step 4: Configure Environment Variables

Click on your backend service → "Variables" tab

Add these variables:

```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"music-app-f2e65",...}
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
APP_ENV=production
```

**IMPORTANT:** 
- `REDIS_URL` is auto-created by Railway (don't add it manually)
- Paste your FULL Firebase JSON (entire content on one line)
- Update `ALLOWED_ORIGINS` with your actual frontend URLs

### Step 5: Deploy

1. Railway will automatically deploy
2. Wait for build to complete (~2-3 minutes)
3. Check logs for any errors

### Step 6: Get Your URL

1. Go to "Settings" tab
2. Click "Generate Domain"
3. Your API will be at: `https://your-app.up.railway.app`

---

## 📋 Detailed Step-by-Step

### 1. Prepare Your Repository

Make sure your code is pushed to GitHub:

```bash
cd musicly-backend
git add .
git commit -m "Ready for Railway deployment"
git push
```

### 2. Railway Project Setup

**A. Create Account**
- Go to https://railway.app
- Click "Login with GitHub"
- Authorize Railway

**B. New Project**
- Dashboard → "New Project"
- "Deploy from GitHub repo"
- Select: `html-proof/Kiro-project`
- Railway detects: Python, Procfile

**C. Project Settings**
- Name: `musicly-backend`
- Region: Choose closest to your users

### 3. Add Redis

**Why Redis?**
- Caching for search results
- Stream URL caching
- Recommendation caching

**How to Add:**
1. Project → "New" → "Database" → "Redis"
2. Railway creates `REDIS_URL` variable automatically
3. No configuration needed!

### 4. Environment Variables

**Required Variables:**

```env
# Firebase Service Account (REQUIRED)
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"music-app-f2e65","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-fbsvc@music-app-f2e65.iam.gserviceaccount.com",...}

# CORS Origins (REQUIRED)
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Environment (REQUIRED)
APP_ENV=production
```

**Auto-Created Variables:**
- `REDIS_URL` - Created by Railway Redis service
- `PORT` - Set by Railway (default: 8000)

**How to Add:**
1. Click your backend service
2. Go to "Variables" tab
3. Click "New Variable"
4. Add each variable
5. Click "Add" for each

### 5. Deployment Configuration

Railway uses your `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Build Process:**
1. Railway detects Python
2. Installs from `requirements.txt`
3. Runs command from `Procfile`
4. Exposes on generated domain

### 6. Monitor Deployment

**Build Logs:**
- Click "Deployments" tab
- View real-time logs
- Check for errors

**Common Build Steps:**
```
→ Installing dependencies from requirements.txt
→ Building application
→ Starting uvicorn server
→ Application ready
```

### 7. Verify Deployment

**Health Check:**
```bash
curl https://your-app.up.railway.app/health
```

**API Docs:**
```
https://your-app.up.railway.app/docs
```

**Test Search:**
```bash
curl "https://your-app.up.railway.app/search?q=test"
```

---

## 🔧 Configuration Details

### Procfile Explained

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

- `web:` - Railway web service
- `uvicorn` - ASGI server
- `app.main:app` - Your FastAPI app
- `--host 0.0.0.0` - Listen on all interfaces
- `--port $PORT` - Use Railway's port

### Requirements.txt

Railway installs all dependencies:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
firebase-admin==6.4.0
redis==5.0.1
yt-dlp==2024.1.0
httpx==0.26.0
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

### Environment Variables Format

**Firebase JSON (Single Line):**
```json
{"type":"service_account","project_id":"music-app-f2e65",...}
```

**CORS Origins (Comma-separated, no spaces):**
```
https://yourdomain.com,https://app.yourdomain.com
```

---

## 🔒 Security Best Practices

### ✅ DO:

1. **Use Environment Variables**
   - Never commit `.env` to Git
   - Store secrets in Railway Variables

2. **Rotate Firebase Keys**
   - Generate new key for production
   - Delete old keys

3. **Set CORS Properly**
   - Only allow your frontend domains
   - No wildcards in production

4. **Monitor Logs**
   - Check for errors
   - Watch for suspicious activity

### ❌ DON'T:

1. **Don't commit secrets**
   - `.env` is in `.gitignore`
   - Firebase JSON not in repo

2. **Don't use test mode**
   - Set `APP_ENV=production`
   - Use production Firebase rules

3. **Don't expose all origins**
   - Specific domains only
   - No `*` in CORS

---

## 📊 Monitoring & Logs

### View Logs

**Real-time:**
- Railway Dashboard → Your Service → "Logs" tab
- Auto-updates as requests come in

**Filter Logs:**
- Click "Filter" to search
- Look for errors or warnings

### Metrics

**Available Metrics:**
- CPU usage
- Memory usage
- Network traffic
- Request count

**Access:**
- Service → "Metrics" tab
- View graphs and stats

### Health Checks

**Endpoint:**
```
GET /health
```

**Response:**
```json
{"status": "healthy"}
```

**Monitor:**
- Set up external monitoring (UptimeRobot, etc.)
- Check every 5 minutes

---

## 🔄 Updates & Redeployment

### Automatic Deployment

Railway auto-deploys on Git push:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Railway automatically:
# 1. Detects push
# 2. Builds new version
# 3. Deploys
# 4. Zero downtime
```

### Manual Deployment

**Redeploy:**
1. Railway Dashboard
2. Your Service → "Deployments"
3. Click "Redeploy"

**Rollback:**
1. "Deployments" tab
2. Find previous deployment
3. Click "Redeploy"

---

## 🐛 Troubleshooting

### Build Fails

**Check:**
1. `requirements.txt` is correct
2. `Procfile` exists
3. Python version compatible

**Fix:**
```bash
# Test locally first
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Application Crashes

**Check Logs:**
- Railway → Logs tab
- Look for Python errors

**Common Issues:**
1. Missing environment variables
2. Redis connection failed
3. Firebase credentials invalid

**Fix:**
- Verify all env vars set
- Check Redis is running
- Test Firebase JSON locally

### Redis Connection Error

**Symptoms:**
```
Connection refused to Redis
```

**Fix:**
1. Check Redis service is running
2. Verify `REDIS_URL` is set
3. Restart both services

### Firebase Error

**Symptoms:**
```
Firebase initialization failed
```

**Fix:**
1. Check `FIREBASE_SERVICE_ACCOUNT_JSON` is complete
2. Verify JSON is valid (no line breaks)
3. Test credentials locally

### CORS Errors

**Symptoms:**
```
Access-Control-Allow-Origin error
```

**Fix:**
1. Add frontend URL to `ALLOWED_ORIGINS`
2. Format: `https://domain1.com,https://domain2.com`
3. No spaces, comma-separated

---

## 💰 Pricing

### Free Tier

**Includes:**
- $5 credit per month
- Enough for small projects
- 500MB RAM
- Shared CPU

**Good For:**
- Development
- Testing
- Small apps

### Paid Plans

**Hobby ($5/month):**
- $5 credit + $5 usage
- Better for production

**Pro ($20/month):**
- $20 credit + usage
- Priority support
- Better performance

**Estimate for Musicly:**
- Backend: ~$3-5/month
- Redis: ~$1-2/month
- Total: ~$5-7/month

---

## 🔗 Useful Links

### Railway

- **Dashboard:** https://railway.app/dashboard
- **Docs:** https://docs.railway.app
- **Status:** https://status.railway.app
- **Discord:** https://discord.gg/railway

### Your Project

- **Repository:** https://github.com/html-proof/Kiro-project
- **Firebase Console:** https://console.firebase.google.com/project/music-app-f2e65

---

## ✅ Deployment Checklist

### Before Deployment

- [ ] Code pushed to GitHub
- [ ] `.env` NOT in repository
- [ ] Firebase credentials ready
- [ ] Frontend URLs known

### During Deployment

- [ ] Railway project created
- [ ] GitHub repo connected
- [ ] Redis database added
- [ ] Environment variables set
- [ ] Build successful
- [ ] Domain generated

### After Deployment

- [ ] Health check passes
- [ ] API docs accessible
- [ ] Test search endpoint
- [ ] Test authentication
- [ ] Monitor logs
- [ ] Set up monitoring

---

## 🎯 Quick Commands

```bash
# Test locally before deploy
uvicorn app.main:app --reload

# Push to GitHub (triggers deploy)
git push

# Test deployed API
curl https://your-app.up.railway.app/health

# View API docs
open https://your-app.up.railway.app/docs
```

---

## 📞 Support

**Railway Issues:**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

**Project Issues:**
- Check TROUBLESHOOTING.md
- Review logs in Railway
- Test locally first

---

**Your backend is ready to deploy! 🚀**

**Next:** Follow Step 1-6 above to deploy to Railway.
