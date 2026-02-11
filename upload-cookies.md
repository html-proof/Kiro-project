# Upload Cookies to Railway - Quick Guide

## The Issue
Your backend is getting "Sign in to confirm you're not a bot" errors from YouTube because Railway's IP is flagged.

## The Solution (Already Implemented!)
The backend code is READY and waiting for cookies.txt. Once you upload it, bot errors will stop.

## Step-by-Step Instructions

### Step 1: Export Cookies from Chrome (2 minutes)

1. **Install the extension:**
   - Go to: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   - Click "Add to Chrome"

2. **Export cookies:**
   - Go to https://youtube.com (make sure you're logged in)
   - Click the extension icon in your toolbar
   - Click "Export" button
   - Save the file as `cookies.txt` to your Downloads folder

### Step 2: Upload to Railway (3 options)

#### Option A: Railway CLI (RECOMMENDED - Most Secure)

```bash
# Install Railway CLI if you haven't
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Upload cookies.txt
railway up cookies.txt
```

#### Option B: Railway Environment Variable (Alternative)

1. Go to your Railway dashboard
2. Select your musicly-backend service
3. Go to "Variables" tab
4. Click "New Variable"
5. Name: `YOUTUBE_COOKIES`
6. Value: Paste the entire contents of cookies.txt
7. Click "Add"

Then update the code to read from environment variable (I can help with this if needed).

#### Option C: Temporary Git Upload (NOT RECOMMENDED - Security Risk)

⚠️ **WARNING:** Only use this for testing, then remove immediately!

```bash
cd musicly-backend

# Copy cookies.txt to the folder
cp ~/Downloads/cookies.txt .

# Force add (it's in .gitignore)
git add -f cookies.txt

# Commit
git commit -m "Add cookies (TEMPORARY - will remove)"

# Push
git push origin main

# Wait for Railway to deploy (check logs)

# IMMEDIATELY remove from git
git rm --cached cookies.txt
git commit -m "Remove cookies from git"
git push origin main
```

### Step 3: Verify It's Working

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Click "View Logs"

**Look for this line:**
```
✅ Using YouTube cookies from: /app/cookies.txt
```

**If you see this instead:**
```
⚠️ No cookies.txt found. Some videos may be blocked by YouTube.
```

Then cookies weren't uploaded correctly. Try again.

### Step 4: Test

Try playing a song that was giving bot errors before. It should work now!

## How Long Do Cookies Last?

- **Typical lifespan:** 2-4 weeks
- **When they expire:** You'll start seeing bot errors again
- **What to do:** Export fresh cookies and re-upload

## Security Notes

- ✅ cookies.txt is already in .gitignore
- ✅ Never commit cookies to public repos
- ✅ Cookies contain your YouTube session
- ✅ Keep them secret
- ✅ Refresh them regularly

## Troubleshooting

### "Railway CLI not found"
```bash
npm install -g @railway/cli
```

### "railway: command not found"
Make sure npm global bin is in your PATH, or use npx:
```bash
npx @railway/cli up cookies.txt
```

### "Still getting bot errors after upload"
1. Check Railway logs - is it finding cookies.txt?
2. Try exporting fresh cookies
3. Make sure you're logged into YouTube when exporting
4. Wait 2-3 minutes for Railway to fully deploy

### "Cookies expired"
Export fresh cookies and re-upload. This is normal and happens every few weeks.

## Alternative: Use Railway Volumes (Advanced)

If Railway supports volumes in your plan:

1. Create a volume in Railway dashboard
2. Mount it to `/app/data`
3. Upload cookies.txt to the volume
4. Update code to look for `/app/data/cookies.txt`

## What Happens After Upload?

1. Railway detects the new file
2. Backend restarts automatically
3. On startup, it checks for cookies.txt
4. If found, all yt-dlp requests use the cookies
5. YouTube sees authenticated requests
6. No more bot detection!

## Current Status

✅ Backend code is ready (cookies + Android client configured)
✅ All you need to do: Upload cookies.txt
✅ Estimated time: 5 minutes total

Once done, your Music Hub will work perfectly with no bot errors!
