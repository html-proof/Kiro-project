# Deployment Guide for Railway.com

## Prerequisites

1. GitHub account
2. Railway.com account
3. Firebase project with service account JSON
4. Redis instance (Railway provides this)

## Step 1: Prepare Firebase Credentials

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download the JSON file
4. Copy the entire JSON content (you'll paste it as an environment variable)

## Step 2: Push to GitHub

```bash
cd musicly-backend
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

## Step 3: Deploy on Railway

1. Go to Railway.com and login
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your musicly-backend repository
5. Railway will auto-detect the Procfile

## Step 4: Add Redis

1. In your Railway project, click "New"
2. Select "Database" → "Redis"
3. Railway will automatically create REDIS_URL environment variable

## Step 5: Set Environment Variables

In Railway dashboard, go to Variables tab and add:

```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"your-project",...}
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
APP_ENV=production
```

Note: REDIS_URL is automatically set by Railway

## Step 6: Deploy

Railway will automatically deploy. Check the logs for any errors.

## Step 7: Get Your API URL

Railway will provide a URL like: `https://musicly-backend-production.up.railway.app`

Use this URL in your Flutter app.

## Testing the Deployment

```bash
curl https://your-railway-url.railway.app/health
```

Should return: `{"status":"healthy"}`

## Monitoring

- Check Railway logs for errors
- Monitor Redis usage
- Set up alerts for high memory/CPU usage

## Scaling

Railway auto-scales based on usage. For high traffic:
- Upgrade Railway plan
- Consider Redis caching optimization
- Monitor yt-dlp performance
