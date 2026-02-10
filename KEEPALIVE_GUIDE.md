# 🔄 Backend Keepalive Configuration

## Problem
Railway containers may sleep after inactivity, causing connection issues.

## Solution
Configure health checks and keepalive pings to keep the backend always active.

---

## ✅ Backend Configuration

### 1. Health Check Endpoint
```
GET /health
GET /ping
```

Both endpoints return status to confirm backend is alive.

### 2. Railway Configuration
In `railway.json`:
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

This tells Railway to check `/health` every 5 minutes.

---

## 🔄 Frontend Keepalive

### For React Native App

Add this to your app to ping the backend every 5 minutes:

```javascript
// In App.js or a service file
import { useEffect } from 'react';
import { AppState } from 'react-native';

const API_BASE = 'https://web-production-1dedc.up.railway.app';

function useBackendKeepalive() {
  useEffect(() => {
    // Ping backend every 5 minutes
    const interval = setInterval(async () => {
      try {
        await fetch(`${API_BASE}/ping`);
      } catch (error) {
        console.log('Keepalive ping failed:', error);
      }
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, []);

  // Also ping when app comes to foreground
  useEffect(() => {
    const subscription = AppState.addEventListener('change', (nextAppState) => {
      if (nextAppState === 'active') {
        fetch(`${API_BASE}/ping`).catch(() => {});
      }
    });

    return () => subscription.remove();
  }, []);
}

// Use in your App component
export default function App() {
  useBackendKeepalive();
  // ... rest of your app
}
```

### For Web App

Add this to your HTML:

```html
<script>
  // Ping backend every 5 minutes
  setInterval(async () => {
    try {
      await fetch('https://web-production-1dedc.up.railway.app/ping');
      console.log('Backend keepalive ping sent');
    } catch (error) {
      console.log('Keepalive ping failed');
    }
  }, 5 * 60 * 1000); // 5 minutes

  // Ping on page load
  fetch('https://web-production-1dedc.up.railway.app/ping').catch(() => {});
</script>
```

---

## 🌐 External Keepalive Services

### Option 1: UptimeRobot (Free)
1. Go to https://uptimerobot.com
2. Create free account
3. Add monitor:
   - Type: HTTP(s)
   - URL: `https://web-production-1dedc.up.railway.app/health`
   - Interval: 5 minutes
4. Done! UptimeRobot will ping your backend every 5 minutes

### Option 2: Cron-job.org (Free)
1. Go to https://cron-job.org
2. Create free account
3. Create new cron job:
   - URL: `https://web-production-1dedc.up.railway.app/ping`
   - Interval: Every 5 minutes
4. Enable the job

### Option 3: Better Uptime (Free)
1. Go to https://betteruptime.com
2. Create free account
3. Add monitor for your backend URL
4. Set check interval to 3-5 minutes

---

## 🎯 Recommended Setup

**Best approach:**
1. ✅ Use UptimeRobot (external keepalive)
2. ✅ Add frontend keepalive (in app)
3. ✅ Railway health checks (already configured)

This triple approach ensures your backend never sleeps!

---

## 📊 How It Works

```
Frontend App
    ↓ (ping every 5 min)
Backend /ping
    ↑
UptimeRobot (ping every 5 min)
    ↑
Railway Health Check (every 5 min)
```

With 3 sources pinging, your backend stays alive 24/7!

---

## ✅ Quick Setup

1. **Deploy backend** (already done)
2. **Sign up for UptimeRobot** (2 minutes)
3. **Add monitor** for your backend URL
4. **Done!** Backend stays alive forever

---

## 🔧 Testing

Test if keepalive works:

```bash
# Ping endpoint
curl https://web-production-1dedc.up.railway.app/ping

# Should return:
# {"status":"alive","timestamp":"ok"}
```

---

## 📝 Summary

✅ **Backend:** Health check endpoints added
✅ **Railway:** Health check configured
✅ **Frontend:** Keepalive code provided
✅ **External:** UptimeRobot recommended

**Your backend will now stay alive 24/7!** 🚀

