# 🔐 Railway Environment Variables Setup

## ✅ PORT Issue Fixed!

Good news: The PORT error is gone! Your app is starting on port 8080.

## ❌ Current Issue: Missing Firebase Credentials

Error: `firebase_service_account_json Field required`

**Solution:** Add environment variables in Railway.

---

## 🚀 Add Environment Variables NOW

### Step 1: Go to Your Railway Project

1. Open: https://railway.app/dashboard
2. Click your project
3. Click your backend service (musicly-backend)

### Step 2: Go to Variables Tab

Click the **"Variables"** tab at the top

### Step 3: Add Required Variables

Click **"New Variable"** and add each of these:

---

### Variable 1: FIREBASE_SERVICE_ACCOUNT_JSON

**Name:**
```
FIREBASE_SERVICE_ACCOUNT_JSON
```

**Value:**
Open your local `.env` file and copy the ENTIRE Firebase JSON (everything after the `=` sign).

It should look like:
```json
{"type":"service_account","project_id":"music-app-f2e65","private_key_id":"8787f0f5e5...","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDiOPxjsCfv7fWD\n...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-fbsvc@music-app-f2e65.iam.gserviceaccount.com","client_id":"117556874740762687400",...}
```

**IMPORTANT:**
- Must be on ONE line
- Include the entire JSON
- No extra quotes
- No line breaks inside the JSON

---

### Variable 2: ALLOWED_ORIGINS

**Name:**
```
ALLOWED_ORIGINS
```

**Value:**
```
https://yourdomain.com,https://app.yourdomain.com
```

Replace with your actual frontend URLs. For testing, you can use:
```
http://localhost:3000,http://localhost:5173,https://yourdomain.com
```

---

### Variable 3: APP_ENV

**Name:**
```
APP_ENV
```

**Value:**
```
production
```

---

### Step 4: Save and Redeploy

After adding all 3 variables:

1. Railway will automatically redeploy
2. Wait for deployment to complete (~2 minutes)
3. Check logs for success

---

## ✅ Verify Variables Are Set

In Railway Variables tab, you should see:

```
FIREBASE_SERVICE_ACCOUNT_JSON = {"type":"service_account"...}
ALLOWED_ORIGINS = https://yourdomain.com,...
APP_ENV = production
REDIS_URL = redis://default:... (auto-created)
PORT = 8080 (auto-created)
```

---

## 🧪 Test After Deployment

Once deployed successfully:

### 1. Check Health Endpoint

```bash
curl https://your-app.up.railway.app/health
```

Should return:
```json
{"status":"healthy"}
```

### 2. Check API Docs

Open in browser:
```
https://your-app.up.railway.app/docs
```

### 3. Test Search

```bash
curl "https://your-app.up.railway.app/search?q=test"
```

---

## 📋 Environment Variables Checklist

- [ ] FIREBASE_SERVICE_ACCOUNT_JSON added (complete JSON)
- [ ] ALLOWED_ORIGINS added (your frontend URLs)
- [ ] APP_ENV added (set to "production")
- [ ] REDIS_URL exists (auto-created by Railway)
- [ ] PORT exists (auto-created by Railway)
- [ ] Deployment successful
- [ ] Health check passes

---

## 🔍 How to Get Firebase JSON

If you don't have it in your `.env` file:

### Option 1: From Your .env File

```bash
# Open your .env file
cat .env

# Copy the value after FIREBASE_SERVICE_ACCOUNT_JSON=
```

### Option 2: Generate New Key

1. Go to: https://console.firebase.google.com/project/music-app-f2e65/settings/serviceaccounts/adminsdk
2. Click "Generate new private key"
3. Download JSON file
4. Open the file
5. Copy ENTIRE content
6. Paste in Railway (on one line)

---

## 🐛 Common Mistakes

### ❌ Wrong: Adding Quotes

```
"{"type":"service_account",...}"
```

### ✅ Correct: No Extra Quotes

```
{"type":"service_account",...}
```

### ❌ Wrong: Line Breaks in JSON

```
{
  "type": "service_account",
  "project_id": "music-app-f2e65"
}
```

### ✅ Correct: Single Line

```
{"type":"service_account","project_id":"music-app-f2e65",...}
```

### ❌ Wrong: Incomplete JSON

```
{"type":"service_account","project_id":"music-app-f2e65"}
```

### ✅ Correct: Complete JSON

```
{"type":"service_account","project_id":"music-app-f2e65","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"...","universe_domain":"googleapis.com"}
```

---

## 📊 Expected Logs After Fix

### Successful Deployment:

```
Starting Musicly Backend on port 8080...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### If Still Failing:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
firebase_service_account_json
  Field required
```

→ Firebase JSON not added or incomplete

---

## 🔄 Force Redeploy

After adding variables, if it doesn't auto-redeploy:

1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Click "Redeploy"

Or trigger from Git:
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

---

## ✅ Success Indicators

After adding variables and redeploying:

1. ✅ Build completes without errors
2. ✅ "Application startup complete" in logs
3. ✅ Service shows "Active" (green dot)
4. ✅ Health endpoint returns 200
5. ✅ API docs load at /docs

---

## 🎯 Quick Summary

**Problem:** Missing Firebase credentials
**Solution:** Add FIREBASE_SERVICE_ACCOUNT_JSON in Railway Variables
**Steps:**
1. Go to Railway → Your Service → Variables
2. Add FIREBASE_SERVICE_ACCOUNT_JSON (complete JSON from .env)
3. Add ALLOWED_ORIGINS (your frontend URLs)
4. Add APP_ENV (set to "production")
5. Wait for redeploy
6. Test health endpoint

---

**Add variables here:** https://railway.app/dashboard

**Your project:** html-proof/Kiro-project

**After adding variables, your app will work!** 🚀
