# Troubleshooting Guide

Common issues and solutions for Musicly Backend.

---

## Installation Issues

### "pip install failed"

**Problem:** Dependencies won't install

**Solutions:**
```bash
# Update pip
python -m pip install --upgrade pip

# Use specific Python version
python3.9 -m pip install -r requirements.txt

# Install with verbose output
pip install -r requirements.txt -v
```

### "yt-dlp not working"

**Problem:** YouTube extraction fails

**Solutions:**
```bash
# Update yt-dlp to latest
pip install -U yt-dlp

# Clear pip cache
pip cache purge
pip install --no-cache-dir yt-dlp
```

---

## Redis Issues

### "Connection refused to Redis"

**Problem:** Cannot connect to Redis

**Solutions:**

**Check if Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

**Start Redis:**
```bash
# Docker
docker run -d -p 6379:6379 redis:latest

# macOS
brew services start redis

# Ubuntu
sudo systemctl start redis

# Windows
# Start redis-server.exe
```

**Check Redis URL:**
```env
# .env file
REDIS_URL=redis://localhost:6379
```

### "Redis memory full"

**Problem:** Redis out of memory

**Solutions:**
```bash
# Clear all cache
redis-cli FLUSHALL

# Check memory usage
redis-cli INFO memory

# Set max memory in redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

---

## Firebase Issues

### "Invalid Firebase credentials"

**Problem:** Firebase authentication fails

**Solutions:**

1. **Check JSON format:**
```env
# Must be valid JSON on single line
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

2. **Verify service account:**
- Go to Firebase Console
- Project Settings → Service Accounts
- Generate new key if needed

3. **Check permissions:**
- Service account needs Firestore and Auth permissions

### "Token verification failed"

**Problem:** User token not accepted

**Solutions:**

1. **Check token format:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

2. **Verify token is fresh:**
- Firebase tokens expire after 1 hour
- Get new token from frontend

3. **Check Firebase project:**
- Ensure using correct project
- Verify Auth is enabled

### "Firestore permission denied"

**Problem:** Cannot read/write Firestore

**Solutions:**

1. **Check Firestore rules:**
```javascript
// Firestore Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

2. **Verify service account permissions**

3. **Check Firestore is enabled in Firebase Console**

---

## API Issues

### "404 Not Found"

**Problem:** Endpoint not found

**Solutions:**

1. **Check URL:**
```bash
# Correct
http://localhost:8000/search?q=test

# Wrong
http://localhost:8000/api/search?q=test
```

2. **Verify server is running:**
```bash
curl http://localhost:8000/health
```

3. **Check route registration in main.py**

### "422 Unprocessable Entity"

**Problem:** Invalid request data

**Solutions:**

1. **Check required parameters:**
```bash
# Missing parameter
curl http://localhost:8000/search
# Error: Field required

# Correct
curl "http://localhost:8000/search?q=test"
```

2. **Verify request body format:**
```bash
# Correct JSON
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"id_token":"your_token"}'
```

### "401 Unauthorized"

**Problem:** Authentication failed

**Solutions:**

1. **Add Authorization header:**
```bash
curl http://localhost:8000/user/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

2. **Get fresh token from Firebase**

3. **Check token format (no extra spaces)**

### "500 Internal Server Error"

**Problem:** Server error

**Solutions:**

1. **Check server logs:**
```bash
# Look for error details in terminal
```

2. **Common causes:**
- Redis not running
- Firebase credentials invalid
- yt-dlp extraction failed
- Network issues

3. **Restart server:**
```bash
# Stop server (Ctrl+C)
# Start again
uvicorn app.main:app --reload
```

---

## YouTube/yt-dlp Issues

### "Video unavailable"

**Problem:** Cannot extract video

**Solutions:**

1. **Update yt-dlp:**
```bash
pip install -U yt-dlp
```

2. **Check video availability:**
- Video might be region-restricted
- Video might be private/deleted
- Age-restricted videos may fail

3. **Try different video ID**

### "Extraction failed"

**Problem:** yt-dlp cannot extract

**Solutions:**

1. **Check internet connection**

2. **Update yt-dlp:**
```bash
pip install --upgrade --force-reinstall yt-dlp
```

3. **Check yt-dlp directly:**
```bash
yt-dlp -F "https://www.youtube.com/watch?v=VIDEO_ID"
```

### "No audio format found"

**Problem:** Cannot find audio stream

**Solutions:**

1. **Video might not have audio**

2. **Try different quality:**
```bash
# Try different quality modes
/resolve?id=VIDEO_ID&quality=high
/resolve?id=VIDEO_ID&quality=ultra
```

3. **Check format availability:**
```bash
yt-dlp -F VIDEO_ID
```

---

## Streaming Issues

### "Stream URL expired"

**Problem:** Stream URL no longer works

**Solutions:**

1. **URLs expire after 15-30 minutes**

2. **Re-resolve the stream:**
```bash
curl "http://localhost:8000/resolve?id=VIDEO_ID"
```

3. **Cache will auto-refresh**

### "Playback stuttering"

**Problem:** Audio/video not smooth

**Solutions:**

1. **Use lower quality:**
```bash
/play?id=VIDEO_ID&quality=ultra
```

2. **Check internet speed**

3. **Use preview mode for testing:**
```bash
/preview?id=VIDEO_ID
```

### "Range requests not working"

**Problem:** Cannot seek in audio/video

**Solutions:**

1. **Check Range header:**
```bash
curl "http://localhost:8000/play?id=VIDEO_ID" \
  -H "Range: bytes=0-1024"
```

2. **Verify proxy service is working**

3. **Check client supports Range requests**

---

## Performance Issues

### "Slow response times"

**Problem:** API is slow

**Solutions:**

1. **Check Redis cache:**
```bash
redis-cli INFO stats
# Look for cache hit rate
```

2. **Monitor yt-dlp:**
- First request is always slower (extraction)
- Subsequent requests use cache

3. **Optimize queries:**
- Use pagination
- Limit result counts
- Enable caching

### "High memory usage"

**Problem:** Server using too much memory

**Solutions:**

1. **Check Redis memory:**
```bash
redis-cli INFO memory
```

2. **Clear cache:**
```bash
redis-cli FLUSHALL
```

3. **Adjust cache TTL in code**

4. **Restart server**

### "Too many requests"

**Problem:** Rate limiting or overload

**Solutions:**

1. **Implement rate limiting**

2. **Increase cache TTL**

3. **Use CDN for static content**

4. **Scale horizontally**

---

## Deployment Issues (Railway)

### "Build failed"

**Problem:** Railway build fails

**Solutions:**

1. **Check Procfile exists:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Verify requirements.txt is complete**

3. **Check build logs for errors**

4. **Ensure Python version compatibility**

### "Environment variables not working"

**Problem:** Config not loading

**Solutions:**

1. **Check variable names (case-sensitive)**

2. **Verify JSON format:**
```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

3. **No quotes around values in Railway**

4. **Restart deployment after changes**

### "Redis connection failed on Railway"

**Problem:** Cannot connect to Railway Redis

**Solutions:**

1. **Check REDIS_URL is set:**
- Should be auto-created by Railway

2. **Verify Redis service is running:**
- Check Railway dashboard

3. **Restart both services**

### "CORS errors in production"

**Problem:** Frontend cannot access API

**Solutions:**

1. **Update ALLOWED_ORIGINS:**
```env
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

2. **Include all frontend URLs**

3. **Redeploy after changes**

4. **Check browser console for exact error**

---

## Database Issues

### "Firestore quota exceeded"

**Problem:** Too many reads/writes

**Solutions:**

1. **Check Firebase Console:**
- Usage tab shows quotas

2. **Optimize queries:**
- Use caching more
- Reduce unnecessary reads
- Batch operations

3. **Upgrade Firebase plan if needed**

### "Data not saving"

**Problem:** Firestore writes fail

**Solutions:**

1. **Check Firestore rules**

2. **Verify user is authenticated**

3. **Check service account permissions**

4. **Look for errors in logs**

---

## Development Issues

### "Module not found"

**Problem:** Import errors

**Solutions:**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Check Python path:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

3. **Verify file structure**

### "Port already in use"

**Problem:** Cannot start server

**Solutions:**

1. **Use different port:**
```bash
uvicorn app.main:app --port 8001
```

2. **Kill existing process:**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 PID
```

3. **Restart terminal**

---

## Testing Issues

### "Tests failing"

**Problem:** test_api.py fails

**Solutions:**

1. **Ensure server is running:**
```bash
curl http://localhost:8000/health
```

2. **Check Redis is running**

3. **Verify environment variables**

4. **Update test video IDs if needed**

---

## Getting Help

### Check Logs
```bash
# Local
# Check terminal output

# Railway
# Check deployment logs in dashboard
```

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

### Test Individual Components
```bash
# Test Redis
redis-cli ping

# Test Firebase
python -c "from app.firebase.firebase_init import initialize_firebase; initialize_firebase()"

# Test yt-dlp
yt-dlp --version
```

### Contact Support
- Railway: https://railway.app/help
- Firebase: https://firebase.google.com/support
- yt-dlp: https://github.com/yt-dlp/yt-dlp/issues

---

## Prevention Tips

1. **Keep dependencies updated:**
```bash
pip install -U yt-dlp
pip list --outdated
```

2. **Monitor regularly:**
- Check logs daily
- Monitor Firebase usage
- Watch Redis memory

3. **Test before deploying:**
- Test locally first
- Use staging environment
- Run test script

4. **Backup important data:**
- Export Firestore data
- Keep service account JSON safe
- Document configuration

5. **Set up alerts:**
- Firebase quota alerts
- Railway resource alerts
- Error monitoring

---

**Still having issues?** Check the other documentation files or create an issue on GitHub.
