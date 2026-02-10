from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional
from app.services.device_manager_service import device_manager


class SyncService:
    """Real-time synchronization service for multi-device playback."""
    
    def __init__(self):
        # Map user_id -> list of websockets
        self.rooms: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, device_id: str = None):
        """Connect a WebSocket for a user."""
        print(f"DEBUG: SyncService.connect starting for {user_id}")
        await websocket.accept()
        print(f"DEBUG: SyncService.connect accepted for {user_id}")
        
        if user_id not in self.rooms:
            self.rooms[user_id] = []
        
        self.rooms[user_id].append(websocket)
        
        # Register device if provided
        if device_id:
            device_manager.register_device(user_id, device_id, {})
        
        print(f"User {user_id} connected. Total connections: {len(self.rooms[user_id])}")
    
    def disconnect(self, websocket: WebSocket, user_id: str, device_id: str = None):
        """Disconnect a WebSocket for a user."""
        if user_id in self.rooms:
            if websocket in self.rooms[user_id]:
                self.rooms[user_id].remove(websocket)
            
            if not self.rooms[user_id]:
                del self.rooms[user_id]
        
        # Remove device if provided
        if device_id:
            device_manager.remove_device(user_id, device_id)
        
        print(f"User {user_id} disconnected.")
    
    async def broadcast_to_user(
        self, 
        user_id: str, 
        message: dict, 
        sender: WebSocket = None
    ):
        """Broadcast a message to all active sessions of a specific user."""
        if user_id in self.rooms:
            for connection in self.rooms[user_id]:
                # Don't send back to the sender
                if sender and connection == sender:
                    continue
                
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to {user_id}: {e}")
    
    async def handle_playback_update(
        self, 
        user_id: str, 
        device_id: str, 
        state: dict, 
        sender: WebSocket = None
    ) -> bool:
        """
        Handle playback state update with device validation.
        Only active device can update playback.
        """
        # Validate device control
        if not device_manager.validate_device_control(user_id, device_id):
            # Send rejection message to sender
            active_device = device_manager.get_active_device(user_id)
            if sender:
                try:
                    await sender.send_json({
                        "type": "playback_controlled_elsewhere",
                        "active_device_id": active_device,
                        "message": "Playback is controlled on another device"
                    })
                except Exception as e:
                    print(f"Error sending rejection: {e}")
            return False
        
        # Update playback state in Firebase
        try:
            from app.firestore.firestore_client import firestore_client
            firestore_client.set_playback_state(user_id, state)
        except Exception as e:
            print(f"Error updating playback state in Firebase: {e}")
        
        # Broadcast to other devices
        await self.broadcast_to_user(
            user_id, 
            {
                "type": "playback_state_update",
                "state": state
            }, 
            sender=sender
        )
        
        return True
    
    async def handle_device_switch(
        self, 
        user_id: str, 
        new_device_id: str
    ) -> bool:
        """Switch active device for a user."""
        success = device_manager.set_active_device(user_id, new_device_id)
        
        if success:
            await self.broadcast_device_switch(user_id, new_device_id)
        
        return success
    
    async def broadcast_device_switch(self, user_id: str, new_active_device_id: str):
        """Broadcast device switch event to all user's devices."""
        await self.broadcast_to_user(
            user_id, 
            {
                "type": "device_switched",
                "active_device_id": new_active_device_id,
                "message": f"Playback control switched to device {new_active_device_id}"
            }
        )
    
    def get_active_device(self, user_id: str) -> Optional[str]:
        """Get the active device for a user."""
        return device_manager.get_active_device(user_id)
    
    def get_user_devices(self, user_id: str) -> List[Dict]:
        """Get all devices for a user."""
        return device_manager.get_user_devices(user_id)


# Export singleton
sync_service = SyncService()
