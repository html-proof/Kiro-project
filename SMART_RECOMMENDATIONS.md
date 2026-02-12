# Smart Recommendation System 🎯

## Overview

Advanced recommendation engine that continuously searches and recommends audio based on:
- ✅ User mood preferences
- ✅ Current date and time (morning/afternoon/evening/night)
- ✅ Trusted YouTube channels
- ✅ View counts and popularity
- ✅ User listening history (excludes already played)
- ✅ Seasonal context (winter/spring/summer/fall)
- ✅ Weekend vs weekday

## Features

### 1. Time-Aware Recommendations ⏰

The system adjusts recommendations based on time of day:

**Morning (5 AM - 12 PM)**
- Energetic, Happy, Motivational, Workout, Upbeat

**Afternoon (12 PM - 5 PM)**
- Focus, Chill, Relaxing, Romantic, Smooth

**Evening (5 PM - 9 PM)**
- Party, Dance, Upbeat, Romantic, Energetic

**Night (9 PM - 5 AM)**
- Chill, Relaxing, Sad, Romantic, Calm

### 2. View-Based Quality Filtering 📊

Three quality levels:

**High Quality** (1M+ views)
- Premium content from major labels
- Verified hits and popular songs
- Best for mainstream listeners

**Medium Quality** (100K+ views) - DEFAULT
- Popular content with proven engagement
- Balance between quality and discovery
- Recommended for most users

**Emerging** (10K+ views)
- Discover new and upcoming artists
- Fresh content before it goes viral
- Best for early adopters

### 3. Trusted Channel Filtering 🏆

Prioritizes content from:

**Global Labels**
- VEVO, Sony Music, Universal Music, Warner Records
- Atlantic Records, Republic Records, Interscope
- Capitol Records, RCA Records, Columbia Records

**Indian Labels**
- T-Series, Zee Music, Saregama, Tips Official
- YRF, Times Music, Sony Music India, Think Music
- Aditya Music, Lahari Music, Anand Audio

**K-Pop / J-Pop**
- HYBE Labels, SM Entertainment, JYP Entertainment
- YG Entertainment, Stone Music, Avex

**Regional Labels**
- Rotana Music, Platinum Records, Mazzika
- Spinnin' Records, Armada Music

### 4. Spam Filtering 🚫

Automatically removes:
- Movie trailers, teasers, scenes
- News, interviews, speeches
- Remixes, DJ mixes, mashups (unless requested)
- 8D audio, slowed/reverb versions
- Karaoke, instrumental versions
- TikTok edits, status videos

### 5. Smart Query Building 🔍

Builds intelligent search queries using:
- User's language preferences
- Mood keywords (18 different moods)
- Current month and year
- Trending keywords
- Weekend/weekday context
- Seasonal context

Example queries:
```
"Tamil romantic trending February 2025 official"
"English energetic weekend hits 2025 official"
"Hindi party trending December 2024 official"
```

## API Endpoints

### 1. Get Smart Recommendations

```http
GET /recommend/smart/recommendations
```

**Query Parameters:**
- `limit` (int, default: 30): Number of recommendations (1-100)
- `quality` (string, default: "medium_quality"): Quality level
  - `high_quality`: 1M+ views
  - `medium_quality`: 100K+ views
  - `emerging`: 10K+ views

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "id": "video_id",
      "title": "Song Title",
      "channel": "Channel Name",
      "views": 1500000,
      "duration": "3:45",
      "thumbnail": "url",
      "trust_score": 90
    }
  ],
  "count": 30,
  "quality_level": "medium_quality",
  "context": {
    "year": 2025,
    "month": "February",
    "day": 12,
    "weekday": "Thursday",
    "time_of_day": "evening",
    "is_weekend": false,
    "season": "winter"
  }
}
```

### 2. Get Continuous Feed (Infinite Scroll)

```http
GET /recommend/smart/feed
```

**Query Parameters:**
- `page` (int, default: 1): Page number
- `page_size` (int, default: 20): Items per page (1-50)

**Response:**
```json
{
  "success": true,
  "songs": [...],
  "page": 1,
  "page_size": 20,
  "total": 20,
  "has_more": true,
  "context": {...}
}
```

### 3. Get Time Context

```http
GET /recommend/smart/time-context
```

**Response:**
```json
{
  "success": true,
  "context": {
    "year": 2025,
    "month": "February",
    "time_of_day": "evening",
    "is_weekend": false,
    "season": "winter"
  },
  "recommended_moods": ["Party", "Dance", "Upbeat", "Romantic", "Energetic"],
  "message": "It's evening on Thursday, February 12, 2025"
}
```

### 4. Get Quality Stats

```http
GET /recommend/smart/quality-stats
```

**Response:**
```json
{
  "success": true,
  "quality_levels": {
    "high_quality": {
      "min_views": 1000000,
      "description": "Premium content with 1M+ views"
    },
    "medium_quality": {
      "min_views": 100000,
      "description": "Popular content with 100K+ views (default)"
    },
    "emerging": {
      "min_views": 10000,
      "description": "Emerging content with 10K+ views"
    }
  },
  "trusted_channels": {
    "global_labels": 18,
    "indian_labels": 18,
    "east_asian_labels": 7,
    "regional_labels": 6,
    "total_trusted": 49
  }
}
```

## How It Works

### Recommendation Flow

1. **Get User Profile**
   - Fetch user's language and mood preferences
   - Get listening history (last 200 songs)

2. **Determine Time Context**
   - Current time of day (morning/afternoon/evening/night)
   - Current date (year, month, day, weekday)
   - Season (winter/spring/summer/fall)
   - Weekend vs weekday

3. **Filter Moods by Time**
   - Match user moods with time-appropriate moods
   - Example: If it's night and user likes "Party", also suggest "Chill"

4. **Build Smart Queries**
   - Combine language + mood + trending keywords
   - Add temporal context (month, year, weekend)
   - Include "official" to prefer official releases

5. **Search YouTube**
   - Execute multiple queries for variety
   - Search for each mood + language combination

6. **Apply Filters**
   - Remove spam and non-music content
   - Filter by trusted channels (trust score ≥ 30)
   - Filter by view count (based on quality level)
   - Exclude already played songs

7. **Sort by Quality**
   - Calculate quality score: 60% trust + 40% views
   - Sort results by quality score

8. **Return Results**
   - Deduplicate by song ID
   - Return top N results

## Usage Examples

### Example 1: Morning Workout Playlist

**User Profile:**
- Languages: English, Tamil
- Moods: Energetic, Workout, Happy
- Time: 7:00 AM (morning)

**System Behavior:**
- Prioritizes: Energetic, Workout, Happy (all match morning)
- Queries:
  - "English energetic trending February 2025 official"
  - "Tamil workout trending February 2025 official"
  - "English happy trending February 2025 official"
- Filters: Medium quality (100K+ views), trusted channels
- Result: 30 high-energy songs perfect for morning workout

### Example 2: Evening Party Mix

**User Profile:**
- Languages: Hindi, English
- Moods: Party, Dance, Romantic
- Time: 8:00 PM (evening)

**System Behavior:**
- Prioritizes: Party, Dance (match evening), Romantic (also matches)
- Queries:
  - "Hindi party weekend trending February 2025 official"
  - "English dance trending February 2025 official"
  - "Hindi romantic trending February 2025 official"
- Filters: Medium quality, trusted channels
- Result: 30 party-ready songs for evening

### Example 3: Night Chill Session

**User Profile:**
- Languages: English
- Moods: Chill, Relaxing, Sad
- Time: 11:00 PM (night)

**System Behavior:**
- Prioritizes: Chill, Relaxing, Sad (all match night)
- Queries:
  - "English chill trending February 2025 official"
  - "English relaxing trending February 2025 official"
  - "English sad trending February 2025 official"
- Filters: Medium quality, trusted channels
- Result: 30 calming songs perfect for late night

## Integration with Flutter App

### 1. Add API Service Method

```dart
// lib/services/api_service.dart

Future<List<Song>> getSmartRecommendations({
  int limit = 30,
  String quality = 'medium_quality',
}) async {
  final response = await get(
    '/recommend/smart/recommendations',
    queryParameters: {
      'limit': limit,
      'quality': quality,
    },
  );
  
  if (response.statusCode == 200) {
    final data = response.data;
    return (data['recommendations'] as List)
        .map((json) => Song.fromJson(json))
        .toList();
  }
  
  throw Exception('Failed to get smart recommendations');
}

Future<Map<String, dynamic>> getSmartFeed({
  int page = 1,
  int pageSize = 20,
}) async {
  final response = await get(
    '/recommend/smart/feed',
    queryParameters: {
      'page': page,
      'page_size': pageSize,
    },
  );
  
  if (response.statusCode == 200) {
    return response.data;
  }
  
  throw Exception('Failed to get smart feed');
}
```

### 2. Create Provider

```dart
// lib/state/smart_recommendation_provider.dart

final smartRecommendationsProvider = FutureProvider.autoDispose<List<Song>>((ref) async {
  final apiService = ref.read(apiServiceProvider);
  return await apiService.getSmartRecommendations(
    limit: 30,
    quality: 'medium_quality',
  );
});

final smartFeedProvider = FutureProvider.family<Map<String, dynamic>, int>(
  (ref, page) async {
    final apiService = ref.read(apiServiceProvider);
    return await apiService.getSmartFeed(page: page, pageSize: 20);
  },
);
```

### 3. Use in UI

```dart
// lib/screens/home/smart_feed_screen.dart

class SmartFeedScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recommendations = ref.watch(smartRecommendationsProvider);
    
    return recommendations.when(
      data: (songs) => ListView.builder(
        itemCount: songs.length,
        itemBuilder: (context, index) {
          final song = songs[index];
          return SongTile(song: song);
        },
      ),
      loading: () => CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}
```

## Performance Considerations

### Caching Strategy

The system uses Redis caching for:
- YouTube search results (4 hours)
- User profile data (1 hour)
- Listening history (30 minutes)

### Optimization Tips

1. **Use pagination** for large result sets
2. **Cache recommendations** on client side for 15-30 minutes
3. **Prefetch next page** when user scrolls to 80% of current page
4. **Use quality levels** appropriately:
   - High quality for premium users
   - Medium quality for regular users
   - Emerging for discovery features

## Monitoring and Debugging

### Debug Logs

Watch for these emoji logs:

```
⏰ Time: evening | Appropriate moods: [Party, Dance, Romantic]
🔍 Smart query: English party trending February 2025 official
📊 Filtered by views (min: 100,000): 45 → 32
🏆 Filtered by trust (min: 30): 32 → 28
🚫 Removed spam: 28 → 25
📈 Sorted by quality score
✨ Smart recommendations: 25 high-quality songs for user123
```

### Common Issues

**No recommendations returned:**
- Check user has completed onboarding
- Verify user has mood preferences set
- Check backend logs for errors

**Low quality results:**
- Increase quality level to "high_quality"
- Check trusted channel configuration
- Verify view count filtering is working

**Same songs repeating:**
- Check listening history is being saved
- Verify played songs are being filtered
- Increase recommendation limit

## Future Enhancements

- [ ] Machine learning for personalized mood detection
- [ ] Collaborative filtering based on similar users
- [ ] Real-time trending detection
- [ ] Genre-based recommendations
- [ ] Artist similarity graph
- [ ] Playlist generation based on activity (workout, study, sleep)
- [ ] Weather-based recommendations
- [ ] Location-based recommendations

## Status: ✅ READY TO USE

All code is complete and ready for testing!
