# Deployment Checklist

## Pre-Deployment

### Firebase Setup
- [ ] Create Firebase project
- [ ] Enable Authentication (Google + Email/Password)
- [ ] Create Firestore database
- [ ] Set Firestore rules for security
- [ ] Generate service account JSON key
- [ ] Copy service account JSON content

### Code Preparation
- [ ] Review all code files
- [ ] Test locally with Redis
- [ ] Verify all endpoints work
- [ ] Check error handling
- [ ] Update ALLOWED_ORIGINS in .env

### GitHub Setup
- [ ] Create GitHub repository
- [ ] Initialize git in project folder
- [ ] Add all files to git
- [ ] Commit and push to GitHub

## Railway Deployment

### Initial Setup
- [ ] Create Railway account
- [ ] Connect GitHub account to Railway
- [ ] Create new project from GitHub repo
- [ ] Verify Procfile is detected

### Database Setup
- [ ] Add Redis database to project
- [ ] Verify REDIS_URL is auto-created
- [ ] Test Redis connection

### Environment Variables
- [ ] Add FIREBASE_SERVICE_ACCOUNT_JSON (full JSON)
- [ ] Add ALLOWED_ORIGINS (your frontend URLs)
- [ ] Set APP_ENV=production
- [ ] Verify REDIS_URL exists

### Deployment
- [ ] Trigger deployment
- [ ] Monitor build logs
- [ ] Check for errors
- [ ] Wait for deployment to complete
- [ ] Copy the Railway app URL

## Post-Deployment Testing

### Basic Tests
- [ ] Test health endpoint: /health
- [ ] Test root endpoint: /
- [ ] Check API docs: /docs
- [ ] Test search endpoint: /search?q=test

### Auth Tests
- [ ] Test login with Firebase token
- [ ] Verify user creation in Firestore
- [ ] Check token validation

### Music Tests
- [ ] Search for songs
- [ ] Resolve audio stream
- [ ] Test audio playback
- [ ] Test preview mode
- [ ] Test video streaming

### User Feature Tests
- [ ] Save preferences
- [ ] Track play history
- [ ] Like songs
- [ ] Save progress
- [ ] Get recommendations

### Playlist Tests
- [ ] Create playlist
- [ ] Add songs to playlist
- [ ] Remove songs
- [ ] Delete playlist
- [ ] Generate auto playlists

## Monitoring Setup

### Railway Dashboard
- [ ] Set up deployment notifications
- [ ] Monitor CPU usage
- [ ] Monitor memory usage
- [ ] Check Redis memory
- [ ] Review logs regularly

### Firebase Console
- [ ] Monitor authentication usage
- [ ] Check Firestore read/write counts
- [ ] Review security rules
- [ ] Set up billing alerts

### Performance
- [ ] Test response times
- [ ] Check cache hit rates
- [ ] Monitor yt-dlp performance
- [ ] Test under load

## Security Checklist

- [ ] Verify CORS is properly configured
- [ ] Check all protected routes require auth
- [ ] Test unauthorized access attempts
- [ ] Verify users can only access their data
- [ ] Review Firestore security rules
- [ ] Check for exposed secrets in code
- [ ] Verify .env is in .gitignore

## Documentation

- [ ] Update README with production URL
- [ ] Document API endpoints
- [ ] Create user guide for frontend team
- [ ] Document environment variables
- [ ] Add troubleshooting guide

## Frontend Integration

- [ ] Share API base URL with frontend team
- [ ] Provide API documentation
- [ ] Test CORS with frontend
- [ ] Verify Firebase token flow
- [ ] Test all endpoints from frontend
- [ ] Check error handling

## Optimization

- [ ] Review cache TTL values
- [ ] Optimize Firestore queries
- [ ] Check Redis memory usage
- [ ] Monitor API response times
- [ ] Optimize yt-dlp settings

## Backup & Recovery

- [ ] Set up Firestore backup
- [ ] Document recovery procedures
- [ ] Test restore process
- [ ] Keep service account JSON secure
- [ ] Document Railway configuration

## Maintenance Plan

- [ ] Schedule yt-dlp updates
- [ ] Plan dependency updates
- [ ] Set up monitoring alerts
- [ ] Create incident response plan
- [ ] Document scaling strategy

## Launch

- [ ] Final smoke test all endpoints
- [ ] Verify all features work
- [ ] Check error logging
- [ ] Monitor first hour of traffic
- [ ] Be ready for quick fixes

## Post-Launch

- [ ] Monitor error rates
- [ ] Check user feedback
- [ ] Review performance metrics
- [ ] Plan feature improvements
- [ ] Document lessons learned

---

## Quick Commands

### Local Testing
```bash
uvicorn app.main:app --reload
```

### Update Dependencies
```bash
pip install -U yt-dlp
pip install -r requirements.txt
```

### Check Redis
```bash
redis-cli ping
```

### Git Push
```bash
git add .
git commit -m "Update"
git push
```

### Railway Logs
Check in Railway dashboard or use Railway CLI

---

## Emergency Contacts

- Railway Support: https://railway.app/help
- Firebase Support: https://firebase.google.com/support
- Team Lead: [Add contact]
- DevOps: [Add contact]

---

## Success Criteria

✅ All endpoints return 200 OK
✅ Authentication works correctly
✅ Music search returns filtered results
✅ Audio streaming works smoothly
✅ Playlists can be created and managed
✅ Recommendations are personalized
✅ Auto playlists generate correctly
✅ Cache is working (check Redis)
✅ No errors in logs
✅ Response times < 2 seconds

---

**Deployment Date:** _____________
**Deployed By:** _____________
**Production URL:** _____________
**Status:** _____________
