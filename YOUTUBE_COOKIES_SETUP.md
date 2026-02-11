# YouTube Cookies Setup - Fix Bot Detection

## Why You Need This

YouTube blocks server IPs (like Railway) with "Sign in to confirm you're not a bot" errors. Using cookies from a real browser session bypasses this completely.

## Quick Setup (5 minutes)

### Step 1: Export Cookies from Browser

**Option A: Using Chrome Extension (Easiest)**
1. Install [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Go to [YouTube.com](https://youtube.com) and make sure you're logged in
3. Click the extension icon
4. Click "Export" → Save as `cookies.txt`

**Option B: Using EditThisCookie**
1. Install [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
2. Go to [YouTube.com](https://youtube.com)
3. Click extension → Options → Export format: Netscape
4. Click "Export" → Save as `cookies.txt`

### Step 2: Upload to Railway

**Via Railway CLI:**
```bash
# In your musicly-backend folder
railway up cookies.txt
```

**Via Git (if cookies.txt is NOT in .gitignore):**
```bash
# Copy cookies.txt to musicly-backend/
cp ~/Downloads/cookies.txt musicly-backend/
cd musicly-backend
git add cookies.txt
git commit -m "Add YouTube cookies"
git push
```

**⚠️ SECURITY WARNING:** Never commit cookies.txt to public repos! Add to .gitignore if repo is public.

### Step 3: Verify It's Working

Check Railway logs after deployment:
```
✅ Using YouTube cookies from: /app/cookies.txt
```

If you see:
```
⚠️ No cookies.txt found. Some videos may be blocked by YouTube.
```

Then cookies.txt wasn't uploaded correctly.

## File Location

The backend looks for cookies.txt in:
```
musicly-backend/
  cookies.txt          ← Put it here
  app/
    main.py
    services/
```

## Cookie Expiration

Cookies expire after a few weeks. If you start seeing bot errors again:
1. Export fresh cookies from browser
2. Upload to Railway again
3. Redeploy

## Testing Locally

```bash
# Make sure cookies.txt is in musicly-backend/
cd musicly-backend
ls cookies.txt  # Should exist

# Run backend
python -m uvicorn app.main:app --reload

# Check logs for:
# ✅ Using YouTube cookies from: cookies.txt
```

## Alternative: Use Android Client Only

If you don't want to manage cookies, the backend now uses Android player client which is less likely to be blocked. But cookies are still the most reliable solution.

## Troubleshooting

**"No such file or directory: cookies.txt"**
- Make sure cookies.txt is in the root of musicly-backend folder
- Check file permissions: `chmod 644 cookies.txt`

**Still getting bot errors**
- Cookies might be expired - export fresh ones
- Make sure you're logged into YouTube when exporting
- Try logging out and back into YouTube, then export again

**Railway deployment fails**
- Don't add cookies.txt to .dockerignore
- Make sure it's committed to git (if using git deploy)
- Or use Railway CLI: `railway up cookies.txt`
