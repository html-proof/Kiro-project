# Firebase Realtime Database Index Fix

## Problem
Backend logs show repeated errors:
```
Index not defined, add ".indexOn": "timestamp", 
for path "/users/bhRpjN3O47eoOvR7IFwSF8R3Jhv2/play_history", to the rules
```

This causes:
- Slow queries on play_history
- Recommendations falling back to "popular songs"
- Performance issues

## Solution

Add index to Firebase Realtime Database rules.

### Step 1: Open Firebase Console
1. Go to https://console.firebase.google.com/
2. Select your project: `sample-music-65323`
3. Click "Realtime Database" in the left menu
4. Click the "Rules" tab

### Step 2: Update Rules

Add the `.indexOn` directive for the `play_history` path:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid",
        "play_history": {
          ".indexOn": ["timestamp"]
        },
        "likes": {
          ".indexOn": ["timestamp"]
        }
      }
    }
  }
}
```

### Step 3: Publish Rules
Click "Publish" button to apply the changes.

## Alternative: Use Firebase CLI

If you have Firebase CLI installed:

```bash
cd musicly-backend
firebase deploy --only database
```

Make sure you have a `database.rules.json` file with the correct rules.

## Expected Result

After adding the index:
- ✅ No more index warnings in logs
- ✅ Faster play_history queries
- ✅ Better recommendations based on user history
- ✅ Improved performance

## Verification

Check backend logs after the fix:
- Should NOT see "Index not defined" errors
- Should see "Got profile data for {uid}" instead of "No profile data"
- Recommendations should be personalized, not just "popular songs"
