from fastapi import APIRouter, Query, Body
from app.services.device_manager_service import device_manager
from app.services.network_monitor_service import network_monitor, audio_output_monitor
from app.utils.response_utils import success_response
from typing import Optional, Dict

router = APIRouter()


# Device Management Routes

@router.post("/register")
async def register_device(
    user_id: str = Query(...),
    device_id: str = Query(...),
    device_info: Dict = Body(...)
):
    """
    Register a new device for a user.
    
    Body: {
        name: string,
        platform: string,
        userAgent: string
    }
    """
    success = device_manager.register_device(user_id, device_id, device_info)
    
    if success:
        return success_response({
            "message": "Device registered successfully",
            "device_id": device_id
        })
    else:
        return {"success": False, "message": "Failed to register device"}


@router.get("/list")
async def list_devices(user_id: str = Query(...)):
    """Get all devices for a user."""
    devices = device_manager.get_user_devices(user_id)
    active_device = device_manager.get_active_device(user_id)
    
    return success_response({
        "devices": devices,
        "active_device_id": active_device
    })


@router.get("/info")
async def get_device_info(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Get information about a specific device."""
    device_info = device_manager.get_device_info(user_id, device_id)
    
    if device_info:
        return success_response(device_info)
    else:
        return {"success": False, "message": "Device not found"}


@router.post("/heartbeat")
async def device_heartbeat(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Update device heartbeat to keep it alive."""
    success = device_manager.update_device_heartbeat(user_id, device_id)
    
    if success:
        return success_response({"message": "Heartbeat updated"})
    else:
        return {"success": False, "message": "Failed to update heartbeat"}


@router.delete("/remove")
async def remove_device(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Remove a device."""
    success = device_manager.remove_device(user_id, device_id)
    
    if success:
        return success_response({"message": "Device removed successfully"})
    else:
        return {"success": False, "message": "Failed to remove device"}


@router.post("/cleanup")
async def cleanup_stale_devices(user_id: str = Query(...)):
    """Clean up stale devices (not seen in >5 minutes)."""
    removed_count = device_manager.cleanup_stale_devices(user_id)
    
    return success_response({
        "message": f"Cleaned up {removed_count} stale device(s)",
        "removed_count": removed_count
    })


# Network Monitoring Routes

@router.post("/network/update")
async def update_network_speed(
    user_id: str = Query(...),
    device_id: str = Query(...),
    speed_mbps: float = Query(...),
    latency_ms: Optional[float] = Query(None)
):
    """
    Update network speed metrics.
    
    Query params:
    - speed_mbps: Download speed in Mbps
    - latency_ms: Optional latency in milliseconds
    """
    success = network_monitor.update_network_speed(
        user_id, 
        device_id, 
        speed_mbps, 
        latency_ms
    )
    
    if success:
        recommended_quality = network_monitor.get_recommended_quality(speed_mbps)
        return success_response({
            "message": "Network speed updated",
            "recommended_quality": recommended_quality
        })
    else:
        return {"success": False, "message": "Failed to update network speed"}


@router.get("/network/info")
async def get_network_info(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Get network information for a device."""
    network_info = network_monitor.get_network_info(user_id, device_id)
    
    if network_info:
        return success_response(network_info)
    else:
        return success_response({
            "speedMbps": None,
            "recommendedQuality": "medium",
            "message": "No network data available"
        })


@router.get("/network/quality")
async def get_adaptive_quality(
    user_id: str = Query(...),
    device_id: str = Query(...),
    requested_quality: Optional[str] = Query(None)
):
    """
    Get adaptive quality recommendation based on network.
    
    Query params:
    - requested_quality: Optional user preference (ultra, high, medium, saver)
    """
    quality = network_monitor.get_adaptive_quality(
        user_id, 
        device_id, 
        requested_quality
    )
    
    return success_response({
        "quality": quality,
        "message": f"Recommended quality: {quality}"
    })


@router.post("/network/connection-type")
async def update_connection_type(
    user_id: str = Query(...),
    device_id: str = Query(...),
    connection_type: str = Query(...)
):
    """
    Update connection type.
    
    Query params:
    - connection_type: wifi, cellular, ethernet, etc.
    """
    success = network_monitor.update_connection_type(
        user_id, 
        device_id, 
        connection_type
    )
    
    if success:
        return success_response({"message": "Connection type updated"})
    else:
        return {"success": False, "message": "Failed to update connection type"}


# Audio Output Routes

@router.post("/audio/output")
async def update_audio_output(
    user_id: str = Query(...),
    device_id: str = Query(...),
    output_info: Dict = Body(...)
):
    """
    Update audio output device.
    
    Body: {
        type: 'headphones' | 'speaker' | 'bluetooth' | 'external',
        name: string (optional),
        isDefault: boolean (optional)
    }
    """
    success = audio_output_monitor.update_audio_output(
        user_id, 
        device_id, 
        output_info
    )
    
    if success:
        return success_response({
            "message": "Audio output updated",
            "output_type": output_info.get('type')
        })
    else:
        return {"success": False, "message": "Failed to update audio output"}


@router.get("/audio/output")
async def get_audio_output(
    user_id: str = Query(...),
    device_id: str = Query(...)
):
    """Get current audio output device information."""
    audio_info = audio_output_monitor.get_audio_output(user_id, device_id)
    
    if audio_info:
        return success_response(audio_info)
    else:
        return success_response({
            "type": "speaker",
            "message": "No audio output data available"
        })


@router.post("/audio/output-change")
async def handle_audio_output_change(
    user_id: str = Query(...),
    device_id: str = Query(...),
    old_output: str = Query(...),
    new_output: str = Query(...)
):
    """
    Handle audio output device change event.
    
    Returns recommendations for handling the change.
    """
    recommendations = audio_output_monitor.handle_output_change(
        user_id,
        device_id,
        old_output,
        new_output
    )
    
    # Update the output in database
    audio_output_monitor.update_audio_output(
        user_id,
        device_id,
        {'type': new_output}
    )
    
    return success_response(recommendations)
