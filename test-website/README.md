# 🧪 Musicly Backend Test Website

## ✅ Test All Recommendation Endpoints

This website lets you test all the backend recommendation features visually!

---

## 🚀 How to Use

### Option 1: Open Directly (Easiest)
Just double-click `index.html` to open in your browser!

### Option 2: Use Python Server
```bash
cd musicly-backend/test-website
python -m http.server 8000
```
Then open: http://localhost:8000

### Option 3: Use Node Server
```bash
cd musicly-backend/test-website
npx serve
```

---

## 🎯 What You Can Test

### 1. Search
- Test the `/search` endpoint
- Search for any song, artist, or keyword
- See filtered results

### 2. Mood Recommendations
- Test `/recommend/type` endpoint
- Try different moods: romantic, party, chill, workout, etc.
- Select language: English, Tamil, Hindi, etc.

### 3. Artist Radio
- Test `/recommend/artist` endpoint
- Enter artist name (e.g., "Anirudh", "Coldplay")
- Get songs by that artist

### 4. Similar Songs
- Test `/recommend/similar` endpoint
- Enter a YouTube video ID
- Get similar songs

---

## 📊 Features

✅ **Real-time Backend Status** - Shows if backend is online
✅ **Beautiful UI** - Gradient design with smooth animations
✅ **Live Results** - See results instantly
✅ **Error Handling** - Clear error messages
✅ **Responsive** - Works on mobile and desktop

---

## 🔗 Backend URL

The website tests this backend:
```
https://web-production-1dedc.up.railway.app
```

---

## 🎨 Screenshots

The website includes:
- Backend status indicator (Online/Offline)
- Search bar with instant results
- Mood selector with language options
- Artist radio with language filter
- Similar songs finder
- Beautiful result cards with thumbnails

---

## ✅ Quick Test

1. Open `index.html` in browser
2. Check if "Backend Online" shows green
3. Click "Search" with default "coldplay" query
4. See results appear!

---

## 🆘 Troubleshooting

### "Backend Offline"
- Check if Railway backend is running
- Test: https://web-production-1dedc.up.railway.app/health

### "No results found"
- Try different search terms
- Check backend logs

### CORS Error
- The backend should have CORS enabled
- If not, run the website through a server (Option 2 or 3)

---

## 📖 Endpoints Tested

```
GET /health                                    - Backend status
GET /search?q={query}                         - Search songs
GET /recommend/type?type={mood}&language={lang} - Mood recommendations
GET /recommend/artist?name={artist}&language={lang} - Artist radio
GET /recommend/similar?id={video_id}          - Similar songs
```

---

## 🎉 Success!

Your backend recommendation system is now visually testable!

Just open `index.html` and start testing! 🚀

