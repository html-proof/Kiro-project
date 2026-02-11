#!/usr/bin/env python3
"""
WebSocket test client for Musicly Backend

Usage:
    python test_websocket.py
"""
import asyncio
import websockets
import json
import sys

async def test_websocket():
    uri = "ws://localhost:8000/ws?user_id=test_user_123"
    
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected!")
            
            # Receive welcome message
            welcome = await websocket.recv()
            print(f"📨 Received: {welcome}")
            
            # Send ping
            print("\n📤 Sending ping...")
            await websocket.send(json.dumps({
                "type": "ping",
                "timestamp": "2024-01-01T00:00:00Z"
            }))
            
            # Receive pong
            pong = await websocket.recv()
            print(f"📨 Received: {pong}")
            
            # Send player state
            print("\n📤 Sending player state...")
            await websocket.send(json.dumps({
                "type": "player_state",
                "data": {
                    "song_id": "abc123",
                    "position": 45.5,
                    "is_playing": True
                }
            }))
            
            # Broadcast message
            print("\n📤 Broadcasting message...")
            await websocket.send(json.dumps({
                "type": "broadcast",
                "data": {
                    "message": "Hello from test client!"
                }
            }))
            
            # Listen for responses
            print("\n👂 Listening for messages (press Ctrl+C to stop)...")
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    print(f"📨 Received: {message}")
                except asyncio.TimeoutError:
                    print("⏱️  No messages received in 5 seconds")
                    break
                    
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Disconnecting...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Musicly WebSocket Test Client")
    print("=" * 50)
    asyncio.run(test_websocket())
