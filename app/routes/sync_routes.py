from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.sync_service import sync_service
from app.utils.response_utils import success_response
from typing import Optional

router = APIRouter()


@router.websocket("/ws/sync")
async def websocket_sync(
    websocket: WebSocket,
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """
    WebSocket endpoint for real-time playback synchronization.
    
    Supports:
    - Multi-device playback control
    - Real-time state synchronization
    - Device switching
    - Playback state updates
    """
    await sync_service.connect(websocket, user_id, device_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "playback_update":
                # Handle playback state update
                state = data.get("state", {})
                await sync_service.handle_playback_update(
                    user_id, 
                    device_id, 
                    state, 
                    sender=websocket
                )
            
            elif message_type == "switch_device":
                # Handle device switch request
                new_device_id = data.get("device_id")
                if new_device_id:
                    success = await sync_service.handle_device_switch(
                        user_id, 
                        new_device_id
                    )
                    await websocket.send_json({
                        "type": "device_switch_response",
                        "success": success
                    })
            
            elif message_type == "ping":
                # Keep-alive ping
                await websocket.send_json({"type": "pong"})
            
            else:
                # Unknown message type
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                })
    
    except WebSocketDisconnect:
        sync_service.disconnect(websocket, user_id, device_id)
        print(f"WebSocket disconnected for user {user_id}, device {device_id}")
    
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {e}")
        sync_service.disconnect(websocket, user_id, device_id)


@router.get("/devices")
async def get_user_devices(user_id: str = Query(...)):
    """Get all devices for a user."""
    devices = sync_service.get_user_devices(user_id)
    active_device = sync_service.get_active_device(user_id)
    
    return success_response({
        "devices": devices,
        "active_device_id": active_device
    })


@router.post("/devices/switch")
async def switch_active_device(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Switch the active device for a user."""
    success = await sync_service.handle_device_switch(user_id, device_id)
    
    if success:
        return success_response({
            "message": "Device switched successfully",
            "active_device_id": device_id
        })
    else:
        return {
            "success": False,
            "message": "Failed to switch device"
        }
