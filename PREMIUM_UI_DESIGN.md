# 🎨 Musicly Premium UI Design Specification

## 🔥 Design Identity: "Aurora Dark + Neon Glass with Vinyl Player"

A unique, premium music streaming app that combines:
- **Aurora Dark** - Flowing northern lights gradients
- **Neon Glass** - Frosted glass cards with glow effects
- **Vinyl Player** - Rotating vinyl disc with needle animation

---

## 🎨 Color Palette

### Primary Colors
```
Background:        #000000 (AMOLED Black)
Card Background:   #121212 (Dark Gray)
Elevated:          #1A1A1A (Medium Gray)
```

### Aurora Gradient
```
Purple:  #8B5CF6
Cyan:    #06B6D4
Pink:    #EC4899
```

### Accent
```
Primary:      #1DB954 (Spotify Green)
Primary Dark: #1AA34A
```

### Text
```
Primary:    #FFFFFF (White)
Secondary:  #B3B3B3 (Light Gray)
Tertiary:   #6B7280 (Medium Gray)
```

### Glass Effect
```
Background: rgba(18, 18, 18, 0.8)
Border:     rgba(255, 255, 255, 0.1)
```

### Mood Colors
```
Romantic:      #EC4899 → #F472B6 (Pink gradient)
Party:         #EF4444 → #F97316 (Red-Orange gradient)
Chill:         #06B6D4 → #0EA5E9 (Cyan gradient)
Workout:       #F59E0B → #EAB308 (Yellow gradient)
Sleep:         #8B5CF6 → #A78BFA (Purple gradient)
Sad:           #6B7280 → #9CA3AF (Gray gradient)
Devotional:    #F59E0B → #FBBF24 (Gold gradient)
Motivational:  #10B981 → #34D399 (Green gradient)
```

---

## 📐 Spacing System

```
XS:   4px   - Tight spacing
SM:   8px   - Small spacing
MD:   16px  - Medium spacing (default)
LG:   24px  - Large spacing
XL:   32px  - Extra large spacing
XXL:  48px  - Huge spacing
```

---

## 🔲 Border Radius

```
SM:   8px   - Small elements
MD:   16px  - Cards
LG:   20px  - Large cards
XL:   28px  - Buttons
Full: 9999px - Circles
```

---

## 📝 Typography

### Font Family
```
Primary: Plus Jakarta Sans (or Inter/SF Pro fallback)
```

### Sizes
```
H1:      32px, Bold      - Page titles
H2:      24px, Semi-Bold - Section titles
H3:      18px, Semi-Bold - Card titles
Body:    16px, Regular   - Main text
Caption: 14px, Regular   - Secondary text
Small:   12px, Regular   - Tertiary text
```

---

## 🎭 Screen Designs

### 1. Splash Screen

**Layout:**
```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│          Aurora Gradient            │
│         (Animated waves)            │
│                                     │
│            ┌───────┐                │
│            │   ♪   │  120x120       │
│            │ Green │  Circle        │
│            └───────┘                │
│                                     │
│           Musicly                   │
│          (48px bold)                │
│                                     │
│         (Loading spinner)           │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- Animated aurora gradient background
- Pulsing logo circle
- Smooth fade-in animation
- Auto-checks login status (2 seconds)

---

### 2. Login Screen

**Layout:**
```
┌─────────────────────────────────────┐
│                                     │
│          Aurora Gradient            │
│         (Top 40% of screen)         │
│                                     │
│            ┌───────┐                │
│            │   ♪   │  120x120       │
│            │ Green │  Circle        │
│            └───────┘                │
│                                     │
│           Musicly                   │
│          (48px bold)                │
│                                     │
│      Your Music, Your Way           │
│         (16px gray)                 │
│                                     │
│                                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  G  Continue with Google    │   │
│  │     (White button)          │   │
│  └─────────────────────────────┘   │
│                                     │
│  By continuing, you agree to our    │
│  Terms of Service and Privacy       │
│         (12px gray)                 │
└─────────────────────────────────────┘
```

**Features:**
- Aurora gradient at top
- Single Google Sign-In button
- Clean, minimal design
- Terms text at bottom

---

### 3. Home Screen (For You)

**Layout:**
```
┌─────────────────────────────────────┐
│ Good Evening, Sebastian    [Avatar] │
│                                     │
│ Continue Listening                  │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐       │
│ │Song│ │Song│ │Song│ │Song│ →     │
│ └────┘ └────┘ └────┘ └────┘       │
│                                     │
│ Auto Playlists                      │
│ ┌──────────┐ ┌──────────┐         │
│ │ On Repeat│ │Daily Mix │ →       │
│ │  [AUTO]  │ │  [AUTO]  │         │
│ └──────────┘ └──────────┘         │
│                                     │
│ Mood Mosaic                         │
│ ┌─────┐ ┌─────┐                    │
│ │ 💗  │ │ 🔥  │                    │
│ │Romnt│ │Party│                    │
│ └─────┘ └─────┘                    │
│ ┌─────┐ ┌─────┐                    │
│ │ 🌙  │ │ ⚡  │                    │
│ │Chill│ │Work │                    │
│ └─────┘ └─────┘                    │
│                                     │
│ 🎵 Smart Data Saver ON              │
└─────────────────────────────────────┘
```

**Features:**
- Greeting with user name
- Continue Listening (horizontal scroll)
- Auto Playlists with "AUTO" badge
- Mood Mosaic (2x4 grid)
- Data Saver badge at bottom
- Aurora gradient background (subtle)

---

### 4. Search Screen

**Layout:**
```
┌─────────────────────────────────────┐
│ ┌─────────────────────────────────┐ │
│ │ 🔍 Search songs, artists...     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Recent Searches                     │
│ • coldplay                          │
│ • imagine dragons                   │
│ • romantic tamil                    │
│                                     │
│ Trending                            │
│ ┌─────────────────────────────────┐ │
│ │ [Img] Song Title                │ │
│ │       Artist Name         [▶]   │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ [Img] Song Title                │ │
│ │       Artist Name         [▶]   │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Features:**
- Floating search bar with blur
- Recent searches
- Instant suggestions
- Results grouped by type
- Play button on each result

---

### 5. Player Screen (Full)

**Layout:**
```
┌─────────────────────────────────────┐
│ [←]                    [❤] [⋮]      │
│                                     │
│                                     │
│        ┌─────────────┐              │
│        │             │              │
│        │   Vinyl     │  Rotating    │
│        │   Disc      │  Animation   │
│        │             │              │
│        │  [Album]    │  Glow Ring   │
│        │             │              │
│        └─────────────┘              │
│                                     │
│         Song Title                  │
│        (24px bold)                  │
│                                     │
│        Artist Name                  │
│        (16px gray)                  │
│                                     │
│ ━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━     │
│ 1:23              3:45              │
│                                     │
│     [🔀]  [⏮]  [▶]  [⏭]  [🔁]     │
│                                     │
│ Quality: [Saver] [High] [Ultra]     │
│                                     │
│ [Similar Songs] [Artist Radio]      │
└─────────────────────────────────────┘
```

**Features:**
- Rotating vinyl disc with album art
- Pulsing glow ring (synced with music)
- Waveform progress bar
- Quality selector
- Similar Songs & Artist Radio buttons
- Video toggle (only on fast internet)

---

### 6. Mini Player (Bottom)

**Layout:**
```
┌─────────────────────────────────────┐
│ [Img] Song Title - Artist    [▶] [❤]│
│ ━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━     │
└─────────────────────────────────────┘
```

**Features:**
- Pinned at bottom of all screens
- Swipe up to expand to full player
- Swipe left/right for next/previous
- Progress bar on top edge
- Slight blur background

---

### 7. Library Screen

**Layout:**
```
┌─────────────────────────────────────┐
│ Library                             │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ❤️ Liked Songs                  │ │
│ │ 127 songs                       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Auto Playlists                      │
│ ┌──────────┐ ┌──────────┐         │
│ │On Repeat│ │Daily Mix │ →       │
│ │  [AUTO] │ │  [AUTO]  │         │
│ └──────────┘ └──────────┘         │
│                                     │
│ Your Playlists                      │
│ ┌─────────────────────────────────┐ │
│ │ [Img] Workout Mix               │ │
│ │       45 songs                  │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ [Img] Chill Vibes               │ │
│ │       32 songs                  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Recently Played                     │
│ (List of recent songs)              │
└─────────────────────────────────────┘
```

**Features:**
- Liked Songs at top (big card)
- Auto Playlists row
- User Playlists grid/list
- Recently Played section
- NO Downloads section

---

## 🎬 Animations

### Must-Have Animations:

1. **Mini Player Expand**
   - Smooth slide up from bottom
   - Album art scales and centers
   - Background blurs

2. **Cover Art Hero**
   - Fade in with scale
   - Glow ring pulses
   - Vinyl rotates when playing

3. **Smooth List Scrolling**
   - Momentum scrolling
   - Bounce effect at edges

4. **Shimmer Loading**
   - Skeleton screens
   - Shimmer effect left to right

5. **Mood Tile Press**
   - Ripple effect
   - Scale down on press

6. **Lyrics Fade-In**
   - Words highlight as they play
   - Smooth scroll to current line

7. **Like Button Bounce**
   - Scale up then down
   - Heart fills with color

8. **Playlist Add Toast**
   - Slide up from bottom
   - Auto-dismiss after 2s

---

## 🎯 Unique Brand Features

### 1. Smart Data Saver Badge
```
Always visible badge showing:
"🎵 Smart Data Saver ON"
"Preview First"
"Video OFF"
```

### 2. Auto Playlist Badge
```
Small "AUTO" badge on auto-generated playlists
Animated glow effect
```

### 3. Mood Mosaic
```
2x4 grid of mood tiles
Each with unique gradient
Icon + name
```

### 4. Vinyl Player
```
Rotating vinyl disc
Needle animation
Album art in center
Glow ring pulses with music
```

### 5. Aurora Background
```
Subtle animated gradient
Purple → Cyan → Pink
Flows slowly in background
```

---

## 📱 Navigation

### Bottom Tab Bar
```
┌─────┬─────┬─────┬─────┐
│ 🏠  │ 🔍  │ 📚  │ 👤  │
│Home │Search│Lib │Profile│
└─────┴─────┴─────┴─────┘
```

**Tabs:**
1. **Home** - For You feed
2. **Search** - Search & discover
3. **Library** - Playlists & likes
4. **Profile** - User settings

---

## 🎨 Component Library

### Glass Card
```javascript
{
  backgroundColor: 'rgba(18, 18, 18, 0.8)',
  borderRadius: 16,
  borderWidth: 1,
  borderColor: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(10px)',
}
```

### Mood Tile
```javascript
{
  width: (screenWidth - 48 - 16) / 2,
  height: 100,
  borderRadius: 20,
  overflow: 'hidden',
  gradient: [color1, color2],
}
```

### Song Row
```javascript
{
  flexDirection: 'row',
  padding: 12,
  backgroundColor: '#121212',
  borderRadius: 12,
  marginBottom: 8,
}
```

### Auto Playlist Card
```javascript
{
  width: 200,
  height: 120,
  borderRadius: 20,
  gradient: ['#8B5CF6', '#06B6D4'],
  badge: 'AUTO',
}
```

---

## ✅ Design Checklist

Before launch, ensure:
- [ ] Aurora gradient animates smoothly
- [ ] Vinyl disc rotates when playing
- [ ] Mini player expands with smooth animation
- [ ] Mood tiles have unique gradients
- [ ] Auto playlists show "AUTO" badge
- [ ] Data Saver badge is visible
- [ ] Glass cards have blur effect
- [ ] All text is readable on dark background
- [ ] Loading states use shimmer
- [ ] Transitions are smooth (60fps)

---

## 🎉 Result

A **premium, unique music streaming app** that:
- Looks like a 2026 app
- Has its own brand identity
- Feels smooth and polished
- Stands out from Spotify
- Users will love using

**Musicly = Aurora Dark + Neon Glass + Vinyl Player** 🔥

