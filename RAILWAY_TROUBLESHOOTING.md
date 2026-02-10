# Railway Deployment Troubleshooting

## Current Issue: Service Unavailable Errors

You're seeing repeated "service unavailable" errors during Railway deployment. This is Railway's internal retry mechanism.

### Common Causes

1. **Railway Service Outage** (Most Likely)
   - Railway's build/deployment service may be experiencing issues
   - Check Railway status: https://status.railway.app/

2. **Build Timeout**
   - Your app is taking too long to build
   - Current healthcheck timeout: 300s (5 minutes)

3. **Startup Failures**
   - App crashes immediately after starting
   - Check Railway logs for Python errors

### Solutions

#### 1. Wait and Retry
If Railway's service is down, just wait 5-10 minutes and the deployment will eventually succeed or fail with a clear error message.

#### 2. Check Railway Logs
```bash
# In Railway dashboard:
1. Go to your project
2. Click on "Deployments"
3. Click on the failing deployment
4. Check "Build Logs" and "Deploy Logs"
```

#### 3. Verify Environment Variables
Make sure these are set in Railway:
- `FIREBASE_CREDENTIALS_JSON` - Your Firebase credentials as JSON string
- `REDIS_URL` - Redis connection URL (optional, will use default if not set)

#### 4. Test Locally First
```bash
cd musicly-backend
python start.py
```

Visit http://localhost:8000/health to verify it works.

#### 5. Reduce Healthcheck Timeout
If builds are timing out, try reducing the timeout in `railway.json`:

```json
{
  "deploy": {
    "healthcheckTimeout": 180
  }
}
```

#### 6. Check Firebase Credentials
The most common startup failure is Firebase credentials:

```bash
# In Railway, verify FIREBASE_CREDENTIALS_JSON is set correctly
# It should be the ENTIRE contents of your Firebase JSON file as a single line
```

### Current Configuration

- **Start Command**: `python start.py`
- **Port**: Automatically detected from Railway's `PORT` environment variable
- **Healthcheck**: `/health` endpoint with 300s timeout
- **Restart Policy**: ON_FAILURE with max 10 retries

### If All Else Fails

1. **Redeploy from scratch**:
   - Delete the current Railway service
   - Create a new one
   - Reconnect to your GitHub repo
   - Set environment variables again

2. **Use Docker instead**:
   - Railway can deploy using your Dockerfile
   - Change builder from NIXPACKS to DOCKERFILE in railway.json

3. **Contact Railway Support**:
   - If the issue persists, it may be a Railway platform issue
   - Check their Discord or support channels

## Recent Changes

Last commit: `e785695` - Fixed duplicate sync_routes import
- This fix should resolve the ImportError that was causing deployment failures
- The current "service unavailable" errors are likely Railway's infrastructure, not your code

## Next Steps

1. Wait for the current deployment to complete (or fail with a clear error)
2. Check Railway's status page
3. Review deployment logs in Railway dashboard
4. If it fails with a Python error, we can fix that
5. If it keeps showing "service unavailable", it's a Railway issue - just wait or try redeploying
