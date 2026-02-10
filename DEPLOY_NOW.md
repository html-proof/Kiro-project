# 🚀 Deploy to Railway NOW!

Quick deployment guide - get your backend live in 5 minutes.

---

## ✅ Security Check First

Run this to verify no secrets in Git:

**Windows:**
```bash
check-security.bat
```

**Linux/Mac:**
```bash
chmod +x check-security.sh
./check-security.sh
```

Should show:
- ✅ .env file is NOT in Git
- ✅ No Firebase JSON files in Git
- ✅ .gitignore configured

---

## 🚀 Deploy Steps

### 1. Push to GitHub (if not done)

```bash
git add .
git commit -m "Ready for deployment"
git push
```

### 2. Go to Railway

Open: https://railway.app

### 3. Create Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: **html-proof/Kiro-project**

### 4. Add Redis

1. Click "New" in your project
2. Select "Database" → "Redis"
3. Done! (REDIS_URL auto-created)

### 5. Add Environment Variables

Click your backend service → "Variables" tab

**Add these 3 variables:**

```
FIREBASE_SERVICE_ACCOUNT_JSON
```
Value: Your complete Firebase JSON (from .env file)

```
ALLOWED_ORIGINS
```
Value: `https://yourdomain.com,https://app.yourdomain.com`

```
APP_ENV
```
Value: `production`

### 6. Generate Domain

1. Go to "Settings" tab
2. Click "Generate Domain"
3. Copy your URL: `https://your-app.up.railway.app`

### 7. Test Your API

```bash
# Health check
curl https://your-app.up.railway.app/health

# API docs
open https://your-app.up.railway.app/docs
```

---

## 🎯 That's It!

Your backend is now live at: `https://your-app.up.railway.app`

---

## 📋 What to Do Next

### Update Frontend

Update your frontend to use the Railway URL:

```javascript
const API_URL = "https://your-app.up.railway.app";
```

### Test Endpoints

```bash
# Search
curl "https://your-app.up.railway.app/search?q=test"

# Health
curl https://your-app.up.railway.app/health
```

### Monitor

- Railway Dashboard → Logs
- Check for errors
- Monitor usage

### Update CORS

Add your actual frontend URLs to `ALLOWED_ORIGINS`:

```
https://yourdomain.com,https://app.yourdomain.com
```

---

## 🔒 Security Checklist

- [ ] `.env` NOT in Git
- [ ] Firebase JSON NOT in Git
- [ ] Environment variables set in Railway
- [ ] CORS configured with real domains
- [ ] Firebase key rotated (if exposed)

---

## 🐛 If Something Goes Wrong

### Build Fails

Check Railway logs:
1. Dashboard → Your Service
2. Click "Deployments"
3. View build logs

### App Crashes

Check runtime logs:
1. Dashboard → Your Service
2. Click "Logs" tab
3. Look for Python errors

### Can't Connect

1. Check service is running (green dot)
2. Verify domain is generated
3. Test health endpoint

---

## 📚 Full Documentation

- **RAILWAY_DEPLOYMENT.md** - Complete guide
- **TROUBLESHOOTING.md** - Common issues
- **API_DOCUMENTATION.md** - API reference

---

## 💰 Cost Estimate

- Backend: ~$3-5/month
- Redis: ~$1-2/month
- **Total: ~$5-7/month**

Free tier includes $5 credit!

---

## 🔗 Quick Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Your Repository:** https://github.com/html-proof/Kiro-project
- **Firebase Console:** https://console.firebase.google.com/project/music-app-f2e65

---

**Ready to deploy? Go to:** https://railway.app 🚀
