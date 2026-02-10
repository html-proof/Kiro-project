# 🚀 React Native App - Quick Start

## ✅ What You Have

A **simple React Native app** with:
- ✅ **Google Sign-In only**
- ✅ **Welcome screen** after login
- ✅ **Spotify-like dark UI**
- ✅ **Connected to your Railway backend**

---

## 🏃 Quick Start (3 Steps)

### 1️⃣ Copy Files

```bash
cd musicly-backend
copy-react-native-files.bat
```

This copies all files to: `C:\Users\seban\personalprojects\musicly-rn\`

### 2️⃣ Update Firebase Config

**IMPORTANT:** Get your Firebase web config!

1. Go to: https://console.firebase.google.com/project/music-app-f2e65
2. Click **⚙️ Project Settings**
3. Scroll to **Your apps** → **Web app**
4. Copy the config

Then update: `C:\Users\seban\personalprojects\musicly-rn\src\config\firebase.js`

```javascript
const firebaseConfig = {
  apiKey: "YOUR_REAL_API_KEY",           // ← Update this
  authDomain: "music-app-f2e65.firebaseapp.com",
  projectId: "music-app-f2e65",
  storageBucket: "music-app-f2e65.firebasestorage.app",
  messagingSenderId: "YOUR_REAL_ID",     // ← Update this
  appId: "YOUR_REAL_APP_ID"              // ← Update this
};
```

### 3️⃣ Run the App

```bash
cd C:\Users\seban\personalprojects\musicly-rn
npm install
npm start
```

Then:
- Press `w` for **web** (easiest for testing)
- Press `a` for **Android** (if emulator running)
- Or scan QR code with **Expo Go** app on your phone

---

## 📱 App Flow

1. **Splash Screen** (2 seconds)
   - Shows Musicly logo
   - Checks if already logged in

2. **Login Screen**
   - Shows "Continue with Google" button
   - User clicks → Google popup
   - After success → Goes to Welcome

3. **Welcome Screen**
   - Shows user's name and avatar
   - Displays "Welcome to Musicly"
   - Has Logout button

---

## 🎨 What It Looks Like

```
┌─────────────────────┐
│   Splash Screen     │
│                     │
│       ♪             │
│     Musicly         │
│    (loading...)     │
└─────────────────────┘
         ↓
┌─────────────────────┐
│   Login Screen      │
│                     │
│       ♪             │
│     Musicly         │
│                     │
│ [Continue with G]   │
└─────────────────────┘
         ↓
┌─────────────────────┐
│  Welcome Screen     │
│                     │
│    [Avatar]         │
│  Welcome to         │
│    Musicly          │
│   John Doe          │
│                     │
│  🎵 Stream Music    │
│  ❤️ Create Playlists│
│  🎧 Discover New    │
│                     │
│    [Logout]         │
└─────────────────────┘
```

---

## 🔧 Files You Need to Know

```
musicly-rn/
├── App.js                          # Main navigation
├── src/
│   ├── config/
│   │   ├── firebase.js            # ← UPDATE THIS!
│   │   └── api.js                 # Backend URL
│   └── screens/
│       ├── SplashScreen.js        # Auto-login check
│       ├── LoginScreen.js         # Google Sign-In
│       └── WelcomeScreen.js       # Welcome page
```

---

## 🆘 Troubleshooting

### "Firebase error"
→ Update `src/config/firebase.js` with real credentials

### "Google Sign-In not working"
→ Enable Google auth in Firebase Console → Authentication

### "Module not found"
```bash
npm install
npm start -- --clear
```

### "Backend error"
→ Check if Railway is running:
```bash
curl https://web-production-1dedc.up.railway.app/health
```

---

## 📦 Build APK

When ready to build Android APK:

```bash
npm install -g eas-cli
eas login
eas build:configure
eas build --platform android --profile preview
```

---

## ✅ That's It!

You now have a working React Native app with Google Sign-In! 🎉

**Next:** Add music search, player, playlists, etc.

All backend APIs are ready at:
```
https://web-production-1dedc.up.railway.app
```

