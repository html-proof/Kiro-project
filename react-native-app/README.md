# 🎵 Musicly React Native App

A beautiful, minimal music streaming app with **Google Sign-In only**.

## ✨ Features

- ✅ Google Sign-In authentication
- ✅ Splash screen with auto-login
- ✅ Welcome screen with user info
- ✅ Spotify-like dark UI
- ✅ Connected to Railway backend

## 🎨 Screenshots

### Splash Screen
```
┌─────────────────────┐
│                     │
│                     │
│       ┌───┐         │
│       │ ♪ │         │  Green circle with music note
│       └───┘         │
│                     │
│     Musicly         │  Large white text
│                     │
│    (loading...)     │  Spinner
│                     │
└─────────────────────┘
```

### Login Screen
```
┌─────────────────────┐
│                     │
│       ┌───┐         │
│       │ ♪ │         │  Green circle
│       └───┘         │
│                     │
│     Musicly         │  Large white text
│  Your Music, Your   │  Gray tagline
│        Way          │
│                     │
│                     │
│                     │
│ ┌─────────────────┐ │
│ │  G  Continue    │ │  White button
│ │  with Google    │ │
│ └─────────────────┘ │
│                     │
│  By continuing, you │  Small gray text
│  agree to our Terms │
└─────────────────────┘
```

### Welcome Screen
```
┌─────────────────────┐
│                     │
│     ┌─────┐         │
│     │     │         │  User avatar
│     └─────┘         │
│                     │
│   Welcome to        │  Gray text
│    Musicly          │  Large green text
│                   │
│   John Doe          │  User name
│  │
│                     │
│ ┌─────────────────┐ │
│ │  🎵             │ │  Feature cards
│ │ Stream Music    │ │
│ │ Listen to       │ │
│ │ millions        │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │  ❤️             │ │
│ │ Create Playlists│ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │  🎧             │ │
│ │ Discover New    │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │    Logout       │ │  Gray button
│ └─────────────────┘ │
└─────────────────────┘
```

## 🔄 App Flow

```
App Start
   ↓
Splash Screen (2s)
   ↓
Check AsyncStorage
   ↓
   ├─ Token Found → Welcome Screen
   │
   └─ No Token → Login Screen
                    ↓
              Click "Continue with Google"
                    ↓
              Firebase Google Auth
                    ↓
              Get ID Token
                    ↓
              POST /auth/login
                    ↓
              Save Token + User Data
                    ↓
              Welcome Screen
                    ↓
              Click "Logout"
                    ↓
              Clear AsyncStorage
                    ↓
              Login Screen
```

## 🚀 Quick Start

1. **Copy files** to your project
2. **Update** `src/config/firebase.js` with real Firebase credentials
3. **Install** dependencies: `npm install`
4. **Run** the app: `npm start`

See `SETUP.md` for detailed instructions!

## 📁 File Structure

```
├── App.js                      # Navigation setup
├── src/
│   ├── config/
│   │   ├── firebase.js        # Firebase config (UPDATE THIS!)
│   │   └── api.js             # Backend API URL
│   └── screens/
│       ├── SplashScreen.js    # Auto-login check
│       ├── LoginScreen.js     # Google Sign-In
│       └── WelcomeScreen.js   # Welcome page
```

## 🎨 Design System

**Colors:**
- Background: `#000000` (Black)
- Accent: `#1DB954` (Spotify Green)
- Card: `#121212` (Dark Gray)
- Button: `#282828` (Medium Gray)
- Text: `#FFFFFF` (White)
- Subtext: `#B3B3B3` (Light Gray)

**Typography:**
- App Name: 48px, Bold
- Welcome: 48px, Bold
- User Name: 24px, Semi-Bold
- Feature Title: 18px, Semi-Bold
- Body: 16px, Regular
- Caption: 14px, Regular

**Spacing:**
- Container Padding: 24px
- Card Padding: 20px
- Button Padding: 16px vertical
- Card Margin: 16px bottom

**Border Radius:**
- Buttons: 30px
- Cards: 16px
- Avatar: 50px (circle)

## 🔗 Backend Integration

**Base URL:**
```
https://web-production-1dedc.up.railway.app
```

**Endpoints Used:**
- `POST /auth/login` - User authentication

**Headers:**
```javascript
{
  'Authorization': 'Bearer <firebase_id_token>'
}
```

## 📦 Dependencies

```json
{
  "@react-navigation/native": "^7.0.13",
  "@react-navigation/stack": "^7.2.1",
  "@react-native-async-storage/async-storage": "^2.1.0",
  "axios": "^1.7.9",
  "expo": "~54.0.0",
  "firebase": "^11.1.0",
  "react-native-screens": "~4.4.0",
  "react-native-safe-area-context": "4.14.0"
}
```

## 🔥 Firebase Setup

1. Go to Firebase Console
2. Get Web app config
3. Update `src/config/firebase.js`
4. Enable Google Sign-In

See `FIREBASE_SETUP.md` for details!

## 📱 Run Commands

```bash
# Start Expo dev server
npm start

# Run on Android
npm run android

# Run on iOS (Mac only)
npm run ios

# Run on Web
npm run web
```

## 🧪 Testing

**Web (Easiest):**
```bash
npm run web
```

**Android Emulator:**
```bash
npm run android
```

**Physical Device:**
1. Install Expo Go app
2. Scan QR code from `npm start`

## 📖 Documentation

- `SETUP.md` - Complete setup guide
- `FIREBASE_SETUP.md` - Firebase configuration
- `../REACT_NATIVE_QUICKSTART.md` - Quick start
- `../REACT_NATIVE_COMPLETE.md` - Full documentation

## ✅ Checklist

Before running:
- [ ] Copy all files to project
- [ ] Update Firebase config in `src/config/firebase.js`
- [ ] Enable Google Sign-In in Firebase Console
- [ ] Run `npm install`
- [ ] Run `npm start`

## 🆘 Troubleshooting

**"Firebase not configured"**
→ Update `src/config/firebase.js` with real values

**"Google Sign-In failed"**
→ Enable Google auth in Firebase Console

**"Module not found"**
→ Run `npm install` and `npm start -- --clear`

**"Backend error"**
→ Check Railway: `curl https://web-production-1dedc.up.railway.app/health`

## 📄 License

MIT

## 🎉 You're Ready!

Your React Native app is complete and ready to run! 🚀

Just update Firebase config and start coding! 🎵

