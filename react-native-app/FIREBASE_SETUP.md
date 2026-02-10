# 🔥 Firebase Setup for React Native App

## Step 1: Get Firebase Web Config

1. Go to **Firebase Console**: https://console.firebase.google.com/project/music-app-f2e65

2. Click the **gear icon** (⚙️) → **Project settings**

3. Scroll down to **Your apps** section

4. If you don't have a Web app yet:
   - Click **Add app** → Select **Web** (</> icon)
   - App nickname: `Musicly Web`
   - Click **Register app**

5. Copy the **firebaseConfig** object

---

## Step 2: Update firebase.js

Open `src/config/firebase.js` and replace with your real values:

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  // ← Your real API key
  authDomain: "music-app-f2e65.firebaseapp.com",
  projectId: "music-app-f2e65",
  storageBucket: "music-app-f2e65.firebasestorage.app",
  messagingSenderId: "123456789012",              // ← Your real sender ID
  appId: "1:123456789012:web:xxxxxxxxxxxxx"      // ← Your real app ID
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
```

---

## Step 3: Enable Google Sign-In

1. In Firebase Console, go to **Authentication**

2. Click **Sign-in method** tab

3. Click **Google** → **Enable**

4. Select support email

5. Click **Save**

---

## Step 4: Add Authorized Domains (for Web)

If testing on web (`npm run web`):

1. Go to **Authentication** → **Settings** → **Authorized domains**

2. Add:
   - `localhost`
   - `127.0.0.1`

---

## Step 5: Test Your Setup

```bash
cd C:\Users\seban\personalprojects\musicly-rn
npm start
```

Press `w` to open in web browser, then:
1. Click "Continue with Google"
2. Select your Google account
3. Should see "Welcome to Musicly" screen!

---

## 🔒 Security Note

**NEVER commit real Firebase credentials to Git!**

The `.gitignore` already excludes `src/config/firebase.js`

---

## ✅ You're Done!

Firebase is now configured for Google Sign-In! 🎉

