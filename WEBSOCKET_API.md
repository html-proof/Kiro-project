# WebSocket API Documentation

## Overview

The Musicly backend provides real-time WebSocket communication for live updates, player synchronization, and notifications.

## Connection

### Endpoint
```
ws://your-domain/ws?user_id=USER_ID
```

### Parameters
- `user_id` (optional): Unique identifier for the user

### Example (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws?user_id=user123');

ws.onopen = () => {
  console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from WebSocket');
};
```

### Example (Python)
```python
import asyncio
import websockets
import json

async def connect():
    uri = "ws://localhost:8000/ws?user_id=user123"
    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(f"Connected: {welcome}")
        
        # Send message
        await websocket.send(json.dumps({
            "type": "ping",
            "timestamp": "2024-01-01T00:00:00Z"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(connect())
```

## Message Types

### 1. Ping/Pong (Keep-Alive)

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

### 2. Broadcast Message

Send a message to all connected clients.

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
  "from": "user123",
  "data": {
    "message": "Hello everyone!"
  }
}
```

### 3. Send to Specific User

Send a message to a specific user.

**Send:**
```json
{
  "type": "send_to_user",
  "target_user": "user456",
  "data": {
    "message": "Private message"
  }
}
```

**Target user receives:**
```json
{
  "type": "message",
  "from": "user123",
  "data": {
    "message": "Private message"
  }
}
```

### 4. Player State Updates

Broadcast player state changes to all clients.

**Send:**
```json
{
  "type": "player_state",
  "data": {
    "song_id": "abc123",
    "title": "Song Title",
    "artist": "Artist Name",
    "position": 45.5,
    "duration": 180.0,
    "is_playing": true,
    "speed": 1.0
  }
}
```

**All clients receive:**
```json
{
  "type": "player_state",
  "user_id": "user123",
  "data": {
    "song_id": "abc123",
    "title": "Song Title",
    "artist": "Artist Name",
    "position": 45.5,
    "duration": 180.0,
    "is_playing": true,
    "speed": 1.0
  }
}
```

## Server-Sent Events

### Connection Established
```json
{
  "type": "connected",
  "message": "Connected to Musicly WebSocket",
  "user_id": "user123",
  "connections": 5
}
```

### User Disconnected
```json
{
  "type": "user_disconnected",
  "user_id": "user456",
  "connections": 4
}
```

### Error
```json
{
  "type": "error",
  "message": "Error description"
}
```

## REST Endpoints

### Get WebSocket Statistics

**GET** `/ws/stats`

**Response:**
```json
{
  "total_connections": 10,
  "unique_users": 8
}
```

## Use Cases

### 1. Real-Time Player Sync
Synchronize playback state across multiple devices for the same user.

### 2. Live Notifications
Send real-time notifications about likes, comments, or playlist updates.

### 3. Collaborative Playlists
Multiple users can see real-time updates when songs are added/removed.

### 4. Presence System
Track which users are currently online and listening.

### 5. Chat/Social Features
Enable real-time messaging between users.

## Error Handling

Always handle connection errors and implement reconnection logic:

```javascript
let ws;
let reconnectInterval = 1000;

function connect() {
  ws = new WebSocket('ws://localhost:8000/ws?user_id=user123');
  
  ws.onopen = () => {
    console.log('Connected');
    reconnectInterval = 1000; // Reset interval
  };
  
  ws.onclose = () => {
    console.log('Disconnected, reconnecting...');
    setTimeout(connect, reconnectInterval);
    reconnectInterval = Math.min(reconnectInterval * 2, 30000); // Exponential backoff
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    ws.close();
  };
}

connect();
```

## Testing

Run the test client:
```bash
python test_websocket.py
```

Or use a WebSocket testing tool like:
- [websocat](https://github.com/vi/websocat)
- [wscat](https://github.com/websockets/wscat)
- Browser DevTools

Example with wscat:
```bash
npm install -g wscat
wscat -c "ws://localhost:8000/ws?user_id=test123"
```
