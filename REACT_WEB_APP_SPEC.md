# 🎵 Musicly React Web App - Complete Specification

## ✅ Production-Ready React Mobile Web App (PWA)

A complete Spotify-like music streaming web app that works perfectly with your FastAPI backend.

---

## 🎯 Core Requirements

### 1. Authentication (Google Only)
- ✅ Firebase Google Sign-In ONLY
- ✅ No email/password login
- ✅ Call `POST /auth/login` with Firebase token
- ✅ Store user data and token
- ✅ Auto-inject token in all API calls

### 2. UI Style (Spotify-Like)
- ✅ Mobile-first responsive design
- ✅ Dark mode default
- ✅ Bottom navigation (Home, Search, Library, Now Playing)
- ✅ Smooth animations
- ✅ Aurora Dark + Neon Glass theme

### 3. Home Screen
- ✅ Continue Listening (`GET /user/recent`)
- ✅ Auto Playlists (`GET /playlist/auto/list`)
- ✅ Recommended For You (`GET /user/recommend`)
- ✅ Mood Mosaic tiles
- ✅ Because You Liked (`GET /recommend/because-liked`)

### 4. Search Screen
- ✅ Real-time search (`GET /search?q=...`)
- ✅ Top 15 filtered results
- ✅ Instant play on click
- ✅ Recent searches cached

### 5. Playback System
- ✅ Audio streaming (`GET /play?id=...&quality=saver`)
- ✅ Quality selector (saver/high/ultra)
- ✅ Preview mode (`GET /preview?id=...`)
- ✅ Progress tracking (`POST /user/progress`)
- ✅ Play tracking (`POST /user/play`)

### 6. Now Playing Screen
- ✅ Large album art
- ✅ Progress seekbar
- ✅ Play/Pause/Next/Previous
- ✅ Like button (`POST /user/like`)
- ✅ Quality selector
- ✅ Repeat/Shuffle toggles
- ✅ Share button

### 7. Library Screen
- ✅ Manual Playlists (`GET /playlist/list`)
- ✅ Auto Playlists (`GET /playlist/auto/list`)
- ✅ Liked Songs (`GET /user/likes`)
- ✅ Recently Played (`GET /user/recent`)
- ✅ Create/Edit/Delete playlists

### 8. Recommendations
- ✅ Mood recommendations (`GET /recommend/type?type=...`)
- ✅ Artist Radio (`GET /recommend/artist?name=...`)
- ✅ Similar Songs (`GET /recommend/similar?id=...`)
- ✅ Because You Liked (`GET /recommend/because-liked`)

### 9. User Preferences
- ✅ Onboarding: Select languages
- ✅ Onboarding: Select favorite artists
- ✅ Save preferences (`POST /user/preferences`)

### 10. Data Saver
- ✅ Data Saver toggle
- ✅ Default quality selector
- ✅ Preview-first mode
- ✅ Video OFF by default

---

## 🛠️ Tech Stack

```
Frontend:
- React 18 + TypeScript
- Vite (fast build)
- TailwindCSS (styling)
- React Router (navigation)
- Zustand (state management)
- React Query (API calls)
- Firebase SDK (auth)
- Howler.js (audio player)

Backend Integration:
- Axios (HTTP client)
- Auto token injection
- Error handling
- Retry logic
```

---

## 📂 Project Structure

```
musicly-web/
├── public/
│   ├── manifest.json
│   └── icons/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── Modal.tsx
│   │   ├── player/
│   │   │   ├── MiniPlayer.tsx
│   │   │   ├── FullPlayer.tsx
│   │   │   └── ProgressBar.tsx
│   │   ├── playlist/
│   │   │   ├── PlaylistCard.tsx
│   │   │   └── PlaylistDetail.tsx
│   │   └── song/
│   │       ├── SongRow.tsx
│   │       └── SongCard.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Search.tsx
│   │   ├── Library.tsx
│   │   ├── Login.tsx
│   │   ├── Onboarding.tsx
│   │   └── NowPlaying.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── usePlayer.ts
│   │   ├── usePlaylist.ts
│   │   └── useSearch.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── player.ts
│   │   └── firebase.ts
│   ├── store/
│   │   ├── authStore.ts
│   │   ├── playerStore.ts
│   │   └── playlistStore.ts
│   ├── types/
│   │   ├── song.ts
│   │   ├── playlist.ts
│   │   └── user.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── theme.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## 🎨 Design System

### Colors
```typescript
const colors = {
  background: '#000000',
  card: '#121212',
  elevated: '#1a1a1a',
  primary: '#1DB954',
  auroraPurple: '#8B5CF6',
  auroraCyan: '#06B6D4',
  auroraPink: '#EC4899',
  text: '#FFFFFF',
  textSecondary: '#B3B3B3',
  textTertiary: '#6B7280',
};
```

### Spacing
```typescript
const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  xxl: '48px',
};
```

### Border Radius
```typescript
const borderRadius = {
  sm: '8px',
  md: '16px',
  lg: '20px',
  xl: '28px',
  full: '9999px',
};
```

---

## 🔌 API Integration

### API Client Setup
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://web-production-1dedc.up.railway.app',
});

// Auto-inject token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Endpoints Used
```typescript
// Auth
POST /auth/login

// Search
GET /search?q={query}

// Playback
GET /resolve?id={id}&quality={quality}
GET /play?id={id}&quality={quality}
GET /preview?id={id}

// User
POST /user/play
POST /user/progress
POST /user/like
POST /user/preferences
GET /user/history
GET /user/recent
GET /user/likes
GET /user/recommend

// Playlists
GET /playlist/list
POST /playlist/create
POST /playlist/add-song
POST /playlist/remove-song
DELETE /playlist/{id}
GET /playlist/{id}

// Auto Playlists
GET /playlist/auto/list
GET /playlist/auto/{id}
POST /playlist/auto/regenerate

// Recommendations
GET /recommend/type?type={mood}&language={lang}
GET /recommend/artist?name={artist}&language={lang}
GET /recommend/similar?id={id}
GET /recommend/because-liked
```

---

## 🎵 Audio Player Implementation

### Player Store (Zustand)
```typescript
interface PlayerState {
  currentSong: Song | null;
  isPlaying: boolean;
  quality: 'saver' | 'high' | 'ultra';
  progress: number;
  duration: number;
  queue: Song[];
  play: (song: Song) => void;
  pause: () => void;
  next: () => void;
  previous: () => void;
  seek: (time: number) => void;
  setQuality: (quality: string) => void;
}
```

### Howler.js Integration
```typescript
import { Howl } from 'howler';

const sound = new Howl({
  src: [streamUrl],
  html5: true,
  format: ['mp3', 'webm'],
  onplay: () => trackPlay(),
  onend: () => playNext(),
  onseek: () => updateProgress(),
});
```

---

## 📱 Screen Implementations

### 1. Login Screen
- Firebase Google Sign-In button
- Aurora gradient background
- Musicly logo
- Auto-redirect if logged in

### 2. Onboarding Screen
- Step 1: Select languages (multi-select)
- Step 2: Select favorite artists (search + chips)
- Save to backend

### 3. Home Screen
- Greeting header
- Continue Listening (horizontal scroll)
- Auto Playlists (cards with AUTO badge)
- Mood Mosaic (2x4 grid)
- Recommended For You (vertical list)
- Because You Liked section

### 4. Search Screen
- Floating search bar
- Recent searches
- Instant results
- Play button on each result

### 5. Library Screen
- Liked Songs (big card)
- Auto Playlists row
- Your Playlists grid
- Recently Played list

### 6. Now Playing Screen
- Large album art with glow
- Song title + artist
- Progress bar with seek
- Play/Pause/Next/Previous
- Like button
- Quality selector
- Similar Songs button
- Artist Radio button

### 7. Mini Player
- Pinned at bottom
- Song info + controls
- Progress bar
- Swipe up to expand

---

## 🚀 Performance Optimizations

1. **Lazy Loading**
   - Code splitting by route
   - Lazy load images

2. **Caching**
   - Cache search results
   - Cache user data
   - Service Worker for offline

3. **Preloading**
   - Preload top 3 search results
   - Preload next song in queue

4. **Debouncing**
   - Search input debounced (300ms)
   - Progress updates throttled

---

## 📦 Build & Deploy

### Development
```bash
npm install
npm run dev
```

### Production Build
```bash
npm run build
npm run preview
```

### Deploy as PWA
```bash
# Build
npm run build

# Deploy to Vercel/Netlify
vercel deploy
# or
netlify deploy
```

---

## ✅ Features Checklist

### Authentication
- [ ] Google Sign-In
- [ ] Auto-login check
- [ ] Token management
- [ ] Logout

### Home
- [ ] Continue Listening
- [ ] Auto Playlists
- [ ] Mood Mosaic
- [ ] Recommendations

### Search
- [ ] Real-time search
- [ ] Recent searches
- [ ] Instant play

### Player
- [ ] Audio streaming
- [ ] Quality selector
- [ ] Preview mode
- [ ] Progress tracking
- [ ] Play tracking

### Library
- [ ] Manual playlists
- [ ] Auto playlists
- [ ] Liked songs
- [ ] Recently played

### Recommendations
- [ ] Mood playlists
- [ ] Artist radio
- [ ] Similar songs
- [ ] Because you liked

### Settings
- [ ] Data saver toggle
- [ ] Quality selector
- [ ] Language preferences

---

## 🎉 Result

A **complete, production-ready React web app** that:
- Works perfectly with your backend
- Looks like Spotify
- Optimized for mobile
- PWA-ready
- Fast and smooth
- Ready to deploy

**Total Files:** ~50 files
**Total Lines:** ~5000+ lines of code
**Time to Build:** Ready to generate!

---

**Ready to generate the complete React app code?** 🚀

