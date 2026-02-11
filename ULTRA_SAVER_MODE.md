# Ultra Saver Mode - 48kbps Instant Streaming

## New Endpoint: `/music/play-48k`

Ultra-compressed 48kbps audio for the slowest connections and maximum data savings.

### Endpoint Details

**URL:** `/music/play-48k`  
**Methods:** GET, POST  
**Parameters:** `id` (YouTube video ID)

**Example:**
```
GET https://your-backend.com/music/play-48k?id=VIDEO_ID
```

## Performance Specs

### File Size Comparison (3-minute song)
| Mode | Bitrate | Size | Savings vs High |
|------|---------|------|-----------------|
| High | 128kbps | 2.9MB | 0% |
| 64k Saver | 64kbps | 1.4MB | 52% |
| **48k Ultra** | **48kbps** | **~1.1MB** | **62%** |

### Latency Optimizations

The transcoder is optimized for instant playback:

1. **No buffering** (`-fflags +nobuffer`)
2. **Low delay mode** (`-flags low_delay`)
3. **Fast encoding** (`-q:a 9`, `-compression_level 0`)
4. **Small chunks** (4KB instead of 8KB)
5. **Auto-reconnect** on network issues

**Target:** First audio chunk in 50-150ms (not 3ms - that's physically impossible due to network latency)

## Quality vs Speed Trade-off

### 48kbps Settings:
- **Sample rate:** 44.1kHz (CD quality)
- **Channels:** Stereo
- **Encoding speed:** Fastest (quality 9)
- **Compression:** Minimal (level 0)

This prioritizes speed over quality. Audio is listenable but not high-fidelity.

## Use Cases

Perfect for:
- 2G/3G connections
- Very slow WiFi
- Background playback
- Podcast-style listening
- Extreme data saving
- High-latency networks

## Flutter Integration

### Add to Music Service

```dart
// music_service.dart
String getUltraSaverStreamUrl(String songId) {
  return '${AppConfig.baseUrl}/music/play-48k?id=$songId';
}
```

### Quality Selector

```dart
enum AudioQuality {
  high,    // 128kbps - Original
  saver,   // 64kbps - Data saver
  ultra,   // 48kbps - Ultra saver
}

String getStreamUrl(String songId, AudioQuality quality) {
  switch (quality) {
    case AudioQuality.ultra:
      return '${AppConfig.baseUrl}/music/play-48k?id=$songId';
    case AudioQuality.saver:
      return '${AppConfig.baseUrl}/music/play-64k?id=$songId';
    case AudioQuality.high:
    default:
      return '${AppConfig.baseUrl}/music/play?id=$songId&quality=high';
  }
}
```

### Auto-detect Connection Speed

```dart
Future<String> getOptimalStreamUrl(String songId) async {
  final speed = await checkConnectionSpeed(); // in Mbps
  
  if (speed < 0.5) {
    // Very slow - use 48kbps
    return '${AppConfig.baseUrl}/music/play-48k?id=$songId';
  } else if (speed < 1.0) {
    // Slow - use 64kbps
    return '${AppConfig.baseUrl}/music/play-64k?id=$songId';
  } else {
    // Normal - use high quality
    return '${AppConfig.baseUrl}/music/play?id=$songId&quality=high';
  }
}
```

## Bandwidth Savings

### Monthly Usage (1000 users, 10 songs/day)

| Mode | Per Song | Daily | Monthly | Cost (@$0.10/GB) |
|------|----------|-------|---------|------------------|
| High (128k) | 2.9MB | 29GB | 870GB | $87 |
| Saver (64k) | 1.4MB | 14GB | 420GB | $42 |
| **Ultra (48k)** | **1.1MB** | **11GB** | **330GB** | **$33** |

**Savings with Ultra mode:** $54/month vs High quality

## Technical Details

### FFmpeg Command
```bash
ffmpeg \
  -reconnect 1 \
  -reconnect_streamed 1 \
  -reconnect_delay_max 2 \
  -i SOURCE_URL \
  -vn \
  -acodec libmp3lame \
  -b:a 48k \
  -q:a 9 \
  -compression_level 0 \
  -ar 44100 \
  -ac 2 \
  -f mp3 \
  -fflags +nobuffer \
  -flags low_delay \
  -
```

### Why Not 3ms?

3 milliseconds is impossible because:
1. **Network latency:** 20-100ms minimum (speed of light)
2. **DNS lookup:** 10-50ms
3. **TLS handshake:** 50-200ms
4. **YouTube fetch:** 100-500ms
5. **FFmpeg startup:** 50-100ms
6. **First chunk encode:** 20-50ms

**Realistic total:** 250-1000ms for first audio

But once streaming starts, chunks arrive every 10-50ms.

## Optimization Tips

### 1. Pre-cache Stream URLs
```dart
// Cache the stream URL before user clicks play
await streamCache.preload(songId);
```

### 2. Reduce Player Buffer
```dart
AudioPlayer(
  audioLoadConfiguration: AudioLoadConfiguration(
    androidLoadControl: AndroidLoadControl(
      minBufferDuration: Duration(milliseconds: 500),
      bufferForPlayback: Duration(milliseconds: 200),
    ),
  ),
)
```

### 3. Show Loading State Immediately
```dart
// Start UI animation instantly
setState(() => isLoading = true);
// Then load audio
await player.setUrl(streamUrl);
```

## Monitoring

Check Railway logs for transcoding performance:
```
Starting FFmpeg MP3 transcode: ... -> 48k (low-latency mode)
```

If you see errors, check:
- FFmpeg is installed (`which ffmpeg`)
- Source URL is valid
- Network connectivity

## Future Improvements

1. **Opus codec:** Better quality at 48kbps than MP3
2. **Pre-transcoding:** Cache popular songs
3. **Adaptive bitrate:** Auto-switch based on connection
4. **WebRTC:** For true low-latency streaming
5. **Edge caching:** CDN for transcoded files

## Comparison with Competitors

| Service | Low Quality | File Size (3min) |
|---------|-------------|------------------|
| Spotify | 24kbps (Opus) | 0.5MB |
| YouTube Music | 48kbps (AAC) | 1.1MB |
| **Music Hub** | **48kbps (MP3)** | **1.1MB** |
| Apple Music | 64kbps (AAC) | 1.4MB |

We match YouTube Music's low-quality mode!
