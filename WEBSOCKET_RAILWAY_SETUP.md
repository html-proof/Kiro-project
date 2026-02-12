# WebSocket Connection - Railway Production

## Production WebSocket URL

```
wss://web-production-1dedc.up.railway.app/ws
```

**Note:** Use `wss://` (WebSocket Secure) for HTTPS connections, not `ws://`

## Connection Examples

### Flutter/Dart
```dart
import 'package:web_socket_channel/web_socket_channel.dart';

final channel = WebSocketChannel.connect(
  Uri.parse('wss://web-production-1dedc.up.railway.app/ws?user_id=USER_ID'),
);

// Listen for messages
channel.stream.listen((message) {
  print('Received: $message');
});

// Send message
channel.sink.add(jsonEncode({
  'type': 'ping',
  'timestamp': DateTime.now().toIso8601String(),
}));

// Close connection
channel.sink.close();
```

### JavaScript (Browser)
```javascript
const ws = new WebSocket('wss://web-production-1dedc.up.railway.app/ws?user_id=USER_ID');

ws.onopen = () => {
  console.log('✅ Connected to Railway WebSocket');
  
  // Send ping
  ws.send(JSON.stringify({
    type: 'ping',
    timestamp: new Date().toISOString()
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('📨 Received:', data);
};

ws.onerror = (error) => {
  console.error('❌ WebSocket error:', error);
};

ws.onclose = () => {
  console.log('🔌 Disconnected');
};
```

### Python
```python
import asyncio
import websockets
import json

async def connect():
    uri = "wss://web-production-1dedc.up.railway.app/ws?user_id=USER_ID"
    
    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(f"✅ Connected: {welcome}")
        
        # Send ping
        await websocket.send(json.dumps({
            "type": "ping",
            "timestamp": "2024-01-01T00:00:00Z"
        }))
        
        # Receive pong
        response = await websocket.recv()
        print(f"📨 Response: {response}")

asyncio.run(connect())
```

### cURL (Testing)
```bash
# Install websocat first: cargo install websocat
websocat "wss://web-production-1dedc.up.railway.app/ws?user_id=TEST123"

# Then send JSON messages:
{"type":"ping","timestamp":"2024-01-01T00:00:00Z"}
```

## Message Types

### 1. Connection Established
When you connect, you'll receive:
```json
{
  "type": "connected",
  "message": "Connected to Musicly WebSocket",
  "user_id": "USER_ID",
  "connections": 5
}
```

### 2. Ping/Pong (Keep-Alive)
**Send:**
```json
{
  "type": "ping",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Receive:**
```json
{
  "type": "pong",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 3. Player State Sync
**Send:**
```json
{
  "type": "player_state",
  "data": {
    "song_id": "VIDEO_ID",
    "title": "Song Title",
    "artist": "Artist Name",
    "position": 45.5,
    "duration": 180.0,
    "is_playing": true,
    "speed": 1.0
  }
}
```

**All connected clients receive:**
```json
{
  "type": "player_state",
  "user_id": "USER_ID",
  "data": {
    "song_id": "VIDEO_ID",
    "title": "Song Title",
    "artist": "Artist Name",
    "position": 45.5,
    "duration": 180.0,
    "is_playing": true,
    "speed": 1.0
  }
}
```

### 4. Broadcast Message
**Send:**
```json
{
  "type": "broadcast",
  "data": {
    "message": "Hello everyone!"
  }
}
```

**All clients receive:**
```json
{
  "type": "broadcast",
  "from": "USER_ID",
  "data": {
    "message": "Hello everyone!"
  }
}
```

### 5. Send to Specific User
**Send:**
```json
{
  "type": "send_to_user",
  "target_user": "TARGET_USER_ID",
  "data": {
    "message": "Private message"
  }
}
```

**Target user receives:**
```json
{
  "type": "message",
  "from": "USER_ID",
  "data": {
    "message": "Private message"
  }
}
```

## Use Cases

### 1. Multi-Device Sync
Sync playback across multiple devices:
```dart
// Device 1 plays a song
channel.sink.add(jsonEncode({
  'type': 'player_state',
  'data': {
    'song_id': 'VIDEO_ID',
    'position': 45.5,
    'is_playing': true
  }
}));

// Device 2 receives and syncs
channel.stream.listen((message) {
  final data = jsonDecode(message);
  if (data['type'] == 'player_state') {
    // Update player state
    playerService.syncState(data['data']);
  }
});
```

### 2. Real-Time Notifications
```dart
// Send notification
channel.sink.add(jsonEncode({
  'type': 'broadcast',
  'data': {
    'notification': 'New song added to playlist',
    'playlist_id': 'PLAYLIST_ID'
  }
}));
```

### 3. Presence System
```dart
// User comes online
channel.sink.add(jsonEncode({
  'type': 'broadcast',
  'data': {
    'event': 'user_online',
    'user_id': 'USER_ID'
  }
}));
```

## Connection Management

### Auto-Reconnect (Flutter)
```dart
class WebSocketService {
  WebSocketChannel? _channel;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  
  void connect(String userId) {
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('wss://web-production-1dedc.up.railway.app/ws?user_id=$userId'),
      );
      
      _channel!.stream.listen(
        (message) {
          _handleMessage(message);
          _reconnectAttempts = 0; // Reset on successful message
        },
        onError: (error) {
          print('WebSocket error: $error');
          _reconnect(userId);
        },
        onDone: () {
          print('WebSocket closed');
          _reconnect(userId);
        },
      );
    } catch (e) {
      print('Connection failed: $e');
      _reconnect(userId);
    }
  }
  
  void _reconnect(String userId) {
    _reconnectAttempts++;
    final delay = Duration(seconds: min(_reconnectAttempts * 2, 30));
    
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(delay, () {
      print('Reconnecting... (attempt $_reconnectAttempts)');
      connect(userId);
    });
  }
  
  void disconnect() {
    _reconnectTimer?.cancel();
    _channel?.sink.close();
  }
}
```

### Heartbeat (Keep-Alive)
```dart
Timer.periodic(Duration(seconds: 30), (timer) {
  channel.sink.add(jsonEncode({
    'type': 'ping',
    'timestamp': DateTime.now().toIso8601String(),
  }));
});
```

## Testing

### 1. Test Connection
```bash
# Using websocat
websocat "wss://web-production-1dedc.up.railway.app/ws?user_id=TEST123"
```

### 2. Test from Browser Console
```javascript
const ws = new WebSocket('wss://web-production-1dedc.up.railway.app/ws?user_id=TEST123');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Received:', e.data);
ws.send(JSON.stringify({type: 'ping', timestamp: new Date().toISOString()}));
```

### 3. Check Connection Stats
```bash
curl https://web-production-1dedc.up.railway.app/ws/stats
```

Response:
```json
{
  "total_connections": 10,
  "unique_users": 8
}
```

## Troubleshooting

### Connection Refused
- ✅ Use `wss://` not `ws://` (secure WebSocket)
- ✅ Check Railway deployment is running
- ✅ Verify URL: `https://web-production-1dedc.up.railway.app/`

### Connection Drops
- ✅ Implement auto-reconnect logic
- ✅ Send periodic ping messages (every 30s)
- ✅ Handle `onclose` and `onerror` events

### Messages Not Received
- ✅ Check JSON format is valid
- ✅ Verify message type is supported
- ✅ Check Railway logs for errors

### CORS Issues
- ✅ WebSocket doesn't use CORS
- ✅ If using HTTP first, ensure CORS is configured
- ✅ Railway backend already has CORS enabled

## Security

### Authentication
Add user authentication:
```dart
final channel = WebSocketChannel.connect(
  Uri.parse('wss://web-production-1dedc.up.railway.app/ws?user_id=$userId&token=$authToken'),
);
```

### Message Validation
Always validate received messages:
```dart
channel.stream.listen((message) {
  try {
    final data = jsonDecode(message);
    if (data['type'] != null) {
      _handleMessage(data);
    }
  } catch (e) {
    print('Invalid message: $e');
  }
});
```

## Production Checklist

- ✅ WebSocket URL: `wss://web-production-1dedc.up.railway.app/ws`
- ✅ Use secure connection (wss://)
- ✅ Implement auto-reconnect
- ✅ Add heartbeat/ping
- ✅ Handle errors gracefully
- ✅ Validate all messages
- ✅ Add authentication (optional)
- ✅ Monitor connection stats

## Current Status

✅ WebSocket server running on Railway  
✅ URL: `wss://web-production-1dedc.up.railway.app/ws`  
✅ Supports multiple connections  
✅ Real-time messaging enabled  
✅ Player state sync ready  
✅ Broadcast functionality working  

---

**Ready to connect! Use `wss://web-production-1dedc.up.railway.app/ws?user_id=YOUR_USER_ID`** 🔌⚡
