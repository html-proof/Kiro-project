# 🎵 Musicly React Native App - Setup Guide

## ✅ What's Included

This is a **simplified React Native app** with:
- ✅ **Google Sign-In Only** (no email/password)
- ✅ **Splash Screen** with auto-login check
- ✅ **Login Screen** with Google button
- ✅ **Welcome Screen** after successful login
- ✅ **Beautiful Spotify-like UI** (dark theme)
- ✅ **Connected to Railway Backend**

---

## 📂 Project Structure

```
musicly-mobile/
├── App.js                          # Main navigation
├── package.json                    # Dependencies
├── app.json                        # Expo config
├── src/
│   ├── config/
│   │   ├── firebase.js            # Firebase config (UPDATE THIS!)
│   │   └── api.js                 # Backend API config
│   └── screens/
│       ├── SplashScreen.js        # Auto-login check
│       ├── LoginScreen.js         # Google Sign-In
│       └── WelcomeScreen.js       # Welcome + Logout
```

---

## 🚀 Setup Instructions

### Step 1: Copy Files to Your Project

Copy all files from `react-native-app/` to:
```
C:\Users\seban\personalprojects\musicly-rn\
```

Or run the batch file:
```bash
copy-react-native-files.bat
```

### Step 2: Update Firebase Config

**IMPORTANT:** Update `src/config/firebase.js` with your real Firebase credentials!

1. Go to: https://console.firebase.google.com/project/music-app-f2e65
2. Click **Project Settings** (gear icon)
3. Scroll to **Your apps** → **Web app**
4. Copy the config values
5. Update `src/config/firebase.js`:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_REAL_API_KEY",
  authDomain: "music-app-f2e65.firebaseapp.com",
  projectId: "music-app-f2e65",
  storageBucket: "music-app-f2e65.firebasestorage.app",
  messagingSenderId: "YOUR_REAL_SENDER_ID",
  appId: "YOUR_REAL_APP_ID"
};
```

### Step 3: Install Dependencies

```bash
cd C:\Users\seban\personalprojects\musicly-rn
npm install
```

### Step 4: Run the App

```bash
# Start Expo
npm start

# Or run directly on Android
npm run android

# Or run on web (for testing)
npm run web
```

---

## 📱 How It Works

### 1. Splash Screen (2 seconds)
- Shows Musicly logo
- Checks if user is already logged in
- Auto-navigates to Welcome or Login

### 2. Login Screen
- Shows "Continue with Google" button
- User clicks → Google Sign-In popup
- After success → Calls backend `/auth/login`
- Saves token → Navigates to Welcome

### 3. Welcome Screen
- Shows user avatar and name
- Displays "Welcome to Musicly"
- Shows 3 feature cards
- Has Logout button

---

## 🎨 UI Features

✅ **Dark Theme** - AMOLED black background
✅ **Spotify Green** - #1DB954 accent color
✅ **Smooth Animations** - Navigation transitions
✅ **User Avatar** - Shows Google profile picture
✅ **Clean Design** - Minimal and modern

---

## 🔗 Backend Connection

The app connects to your Railway backend:
```
https://web-production-1dedc.up.railway.app
```

When user logs in:
1. Firebase authenticates with Google
2. App gets Firebase ID token
3. App calls `POST /auth/login` with token
4. Backend validates and returns user data
5. App saves token and navigates to Welcome

---

## 🧪 Test the App

### On Web (Easiest):
```bash
npm run web
```
Opens in browser at `http://localhost:8081`

### On Android Emulator:
```bash
npm run android
```
Make sure Android emulator is running!

### On Physical Device:
1. Install **Expo Go** app from Play Store
2. Run `npm start`
3. Scan QR code with Expo Go
4. App loads on your phone!

---

## 🔧 Troubleshooting

### "Firebase not configured"
- Update `src/config/firebase.js` with real values
- Get them from Firebase Console

### "Google Sign-In not working"
- Make sure Firebase has Google auth enabled
- Check Firebase Console → Authentication → Sign-in method

### "Backend error"
- Check if Railway backend is running
- Test: `curl https://web-production-1dedc.up.railway.app/health`

### "Module not found"
```bash
npm install
npm start -- --clear
```

---

## 📦 Build APK (Android)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure build
eas build:configure

# Build APK
eas build --platform android --profile preview
```

APK will be available for download after build completes!

---

## 🎯 What's Next?

After login works, you can add:
- 🎵 Music search screen
- 🎧 Audio player
- ❤️ Favorites/Likes
- 📱 Playlists
- 🔍 Search functionality

All backend APIs are ready at:
```
https://web-production-1dedc.up.railway.app
```

---

## ✅ Summary

You now have a **complete React Native app** with:
- ✅ Google Sign-In
- ✅ Welcome screen
- ✅ Beautiful UI
- ✅ Backend integration
- ✅ Ready to run!

**Just update Firebase config and run:** `npm start` 🚀

