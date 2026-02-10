# 🎵 Musicly Flutter App - Complete Setup Guide

## 📱 Create Your Flutter Project

### Step 1: Create Flutter Project

```bash
# Navigate to your projects folder
cd C:\Users\seban\personalprojects

# Create Flutter project
flutter create musicly_app

# Navigate into project
cd musicly_app
```

### Step 2: Update pubspec.yaml

Replace the dependencies section with:

```yaml
name: musicly_app
description: Premium music streaming app
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.9
  
  # Firebase
  firebase_core: ^2.24.2
  firebase_auth: ^4.15.3
  google_sign_in: ^6.1.6
  
  # Networking
  dio: ^5.4.0
  retrofit: ^4.0.3
  json_annotation: ^4.8.1
  
  # Audio/Video
  just_audio: ^0.9.36
  just_audio_background: ^0.0.1-beta.11
  audio_service: ^0.18.12
  video_player: ^2.8.1
  
  # UI/Animations
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0
  flutter_animate: ^4.3.0
  lottie: ^2.7.0
  
  # Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  shared_preferences: ^2.2.2
  
  # Utils
  get_it: ^7.6.4
  connectivity_plus: ^5.0.2
  permission_handler: ^11.1.0
  intl: ^0.18.1
  uuid: ^4.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  build_runner: ^2.4.7
  json_serializable: ^6.7.1
  retrofit_generator: ^8.0.4
  hive_generator: ^2.0.1

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/animations/
    - assets/icons/
  
  fonts:
    - family: Circular
      fonts:
        - asset: assets/fonts/CircularStd-Book.otf
        - asset: assets/fonts/CircularStd-Bold.otf
          weight: 700
```

### Step 3: Install Dependencies

```bash
flutter pub get
```

### Step 4: Configure Firebase

1. **Download Firebase Config Files:**
   - Go to Firebase Console: https://console.firebase.google.com/project/music-app-f2e65
   - Add Android app (package: `com.musicly.app`)
   - Download `google-services.json` → Place in `android/app/`
   - Add iOS app (optional)
   - Download `GoogleService-Info.plist` → Place in `ios/Runner/`

2. **Update android/build.gradle:**
```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

3. **Update android/app/build.gradle:**
```gradle
apply plugin: 'com.google.gms.google-services'

android {
    defaultConfig {
        minSdkVersion 21
        targetSdkVersion 34
    }
}
```

### Step 5: Update API Configuration

Create `lib/core/config/api_config.dart`:

```dart
class ApiConfig {
  static const String baseUrl = 'https://web-production-1dedc.up.railway.app';
  
  // Your actual Railway URL
  static const String apiUrl = baseUrl;
}
```

### Step 6: Run the App

```bash
# Check devices
flutter devices

# Run on Android
flutter run

# Build APK
flutter build apk --release

# Build App Bundle
flutter build appbundle --release
```

## 📁 Project Structure

```
musicly_app/
├── lib/
│   ├── main.dart
│   ├── core/
│   │   ├── config/
│   │   │   ├── api_config.dart
│   │   │   └── theme_config.dart
│   │   ├── di/
│   │   │   └── injection.dart
│   │   ├── network/
│   │   │   ├── api_client.dart
│   │   │   └── dio_client.dart
│   │   └── utils/
│   │       ├── constants.dart
│   │       └── helpers.dart
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── home/
│   │   ├── search/
│   │   ├── player/
│   │   ├── library/
│   │   └── playlist/
│   └── shared/
│       ├── models/
│       ├── widgets/
│       └── providers/
├── assets/
│   ├── images/
│   ├── animations/
│   └── fonts/
└── test/
```

## 🎨 Design System

### Colors
- Primary: `#1DB954` (Spotify Green)
- Background: `#121212` (AMOLED Black)
- Surface: `#181818`
- Accent: Purple-Blue Gradient

### Typography
- Font: Circular Std (Spotify's font)
- Fallback: Roboto

## 🔥 Key Features Implemented

✅ Firebase Authentication (Google + Email)
✅ Music Search with Filters
✅ Audio Streaming with Quality Selection
✅ Mini Player + Full Player
✅ Playlists (Manual + Auto)
✅ Recommendations
✅ Offline Support
✅ Background Playback
✅ Progress Tracking
✅ Like/Unlike Songs
✅ History Tracking

## 🚀 Next Steps

1. Run `flutter create musicly_app`
2. Copy all the code files I'll provide
3. Update `pubspec.yaml`
4. Add Firebase config files
5. Run `flutter pub get`
6. Run the app!

## 📱 Build & Release

### Android APK
```bash
flutter build apk --release --split-per-abi
```

### Android App Bundle (for Play Store)
```bash
flutter build appbundle --release
```

### iOS (requires Mac)
```bash
flutter build ios --release
```

---

**Ready to build!** I'll now create all the Flutter code files.
