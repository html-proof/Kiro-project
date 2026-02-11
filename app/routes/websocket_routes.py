from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.connection_manager import manager
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = Query(None)
):
    """
    WebSocket endpoint for real-time communication
    
    Usage:
    - Connect: ws://your-domain/ws?user_id=USER_ID
    - Send JSON messages: {"type": "message", "data": {...}}
    - Receive JSON messages: {"type": "notification", "data": {...}}
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to Musicly WebSocket",
            "user_id": user_id,
            "connections": manager.get_connection_count()
        })
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")
                
                logger.info(f"Received WebSocket message from {user_id}: {message_type}")
                
                # Handle different message types
                if message_type == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    })
                
                elif message_type == "broadcast":
                    # Broadcast to all users
                    await manager.broadcast({
                        "type": "broadcast",
                        "from": user_id,
                        "data": message.get("data")
                    })
                
                elif message_type == "send_to_user":
                    # Send to specific user
                    target_user = message.get("target_user")
                    if target_user:
                        await manager.send_personal_message({
                            "type": "message",
                            "from": user_id,
                            "data": message.get("data")
                        }, target_user)
                
                elif message_type == "player_state":
                    # Broadcast player state changes
                    await manager.broadcast({
                        "type": "player_state",
                        "user_id": user_id,
                        "data": message.get("data")
                    })
                
                else:
                    # Echo back unknown messages
                    await websocket.send_json({
                        "type": "echo",
                        "original": message
                    })
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"WebSocket disconnected: {user_id}")
        
        # Notify others about disconnection
        await manager.broadcast({
            "type": "user_disconnected",
            "user_id": user_id,
            "connections": manager.get_connection_count()
        })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)

@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "total_connections": manager.get_connection_count(),
        "unique_users": manager.get_user_count()
    }
