from typing import Dict, Optional
import time
from firebase_admin import db


class NetworkMonitor:
    """
    Network speed monitoring and adaptive quality selection.
    
    Features:
    - Track network speed per user/device
    - Recommend optimal quality based on connection
    - Store network metrics in Firebase
    """
    
    # Quality thresholds (Mbps)
    QUALITY_THRESHOLDS = {
        'ultra': 2.0,    # 320kbps audio
        'high': 1.0,     # 192kbps audio
        'medium': 0.5,   # 128kbps audio
        'saver': 0.0     # 64kbps audio
    }
    
    def __init__(self):
        self.speed_cache = {}  # In-memory cache for quick access
    
    def update_network_speed(
        self, 
        user_id: str, 
        device_id: str, 
        speed_mbps: float,
        latency_ms: Optional[float] = None
    ) -> bool:
        """
        Update network speed metrics for a user's device.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            speed_mbps: Download speed in Mbps
            latency_ms: Optional latency in milliseconds
            
        Returns:
            True if successful, False otherwise
        """
        if not user_id or not device_id:
            return False
        
        try:
            ref = db.reference(f'users/{user_id}/devices/{device_id}/network')
            
            network_data = {
                'speedMbps': round(speed_mbps, 2),
                'timestamp': {'.sv': 'timestamp'},
                'recommendedQuality': self.get_recommended_quality(speed_mbps)
            }
            
            if latency_ms is not None:
                network_data['latencyMs'] = round(latency_ms, 2)
            
            ref.update(network_data)
            
            # Update cache
            cache_key = f"{user_id}:{device_id}"
            self.speed_cache[cache_key] = {
                'speed': speed_mbps,
                'quality': network_data['recommendedQuality'],
                'timestamp': time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"Error updating network speed: {e}")
            return False
    
    def get_recommended_quality(self, speed_mbps: float) -> str:
        """
        Get recommended audio quality based on network speed.
        
        Args:
            speed_mbps: Download speed in Mbps
            
        Returns:
            Quality level: 'ultra', 'high', 'medium', or 'saver'
        """
        if speed_mbps >= self.QUALITY_THRESHOLDS['ultra']:
            return 'ultra'
        elif speed_mbps >= self.QUALITY_THRESHOLDS['high']:
            return 'high'
        elif speed_mbps >= self.QUALITY_THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'saver'
    
    def get_network_info(
        self, 
        user_id: str, 
        device_id: str
    ) -> Optional[Dict]:
        """
        Get network information for a device.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            
        Returns:
            Network info dictionary or None
        """
        if not user_id or not device_id:
            return None
        
        # Check cache first
        cache_key = f"{user_id}:{device_id}"
        if cache_key in self.speed_cache:
            cached = self.speed_cache[cache_key]
            # Cache valid for 5 minutes
            if time.time() - cached['timestamp'] < 300:
                return {
                    'speedMbps': cached['speed'],
                    'recommendedQuality': cached['quality'],
                    'cached': True
                }
        
        # Fetch from Firebase
        try:
            ref = db.reference(f'users/{user_id}/devices/{device_id}/network')
            network_data = ref.get()
            
            if network_data:
                return {
                    'speedMbps': network_data.get('speedMbps'),
                    'latencyMs': network_data.get('latencyMs'),
                    'recommendedQuality': network_data.get('recommendedQuality'),
                    'timestamp': network_data.get('timestamp'),
                    'cached': False
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting network info: {e}")
            return None
    
    def get_adaptive_quality(
        self, 
        user_id: str, 
        device_id: str,
        requested_quality: Optional[str] = None
    ) -> str:
        """
        Get adaptive quality based on network conditions.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            requested_quality: User's preferred quality (optional)
            
        Returns:
            Quality level to use
        """
        network_info = self.get_network_info(user_id, device_id)
        
        if not network_info:
            # No network info, use requested or default to medium
            return requested_quality or 'medium'
        
        recommended = network_info.get('recommendedQuality', 'medium')
        
        # If user requested a quality, use the lower of requested vs recommended
        if requested_quality:
            quality_order = ['saver', 'medium', 'high', 'ultra']
            requested_idx = quality_order.index(requested_quality) if requested_quality in quality_order else 1
            recommended_idx = quality_order.index(recommended) if recommended in quality_order else 1
            
            # Use the lower quality to ensure smooth playback
            return quality_order[min(requested_idx, recommended_idx)]
        
        return recommended
    
    def update_connection_type(
        self, 
        user_id: str, 
        device_id: str,
        connection_type: str
    ) -> bool:
        """
        Update connection type (wifi, cellular, ethernet, etc.).
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            connection_type: Type of connection
            
        Returns:
            True if successful, False otherwise
        """
        if not user_id or not device_id:
            return False
        
        try:
            ref = db.reference(f'users/{user_id}/devices/{device_id}/network')
            ref.update({
                'connectionType': connection_type,
                'timestamp': {'.sv': 'timestamp'}
            })
            
            return True
            
        except Exception as e:
            print(f"Error updating connection type: {e}")
            return False


class AudioOutputMonitor:
    """
    Audio output device monitoring and management.
    
    Features:
    - Track audio output device changes
    - Store output preferences
    - Handle headphone/speaker switching
    """
    
    def update_audio_output(
        self,
        user_id: str,
        device_id: str,
        output_info: Dict
    ) -> bool:
        """
        Update audio output device information.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            output_info: {
                type: 'headphones' | 'speaker' | 'bluetooth' | 'external',
                name: Device name (optional),
                isDefault: boolean
            }
            
        Returns:
            True if successful, False otherwise
        """
        if not user_id or not device_id:
            return False
        
        try:
            ref = db.reference(f'users/{user_id}/devices/{device_id}/audioOutput')
            
            audio_data = {
                'type': output_info.get('type', 'speaker'),
                'timestamp': {'.sv': 'timestamp'}
            }
            
            if output_info.get('name'):
                audio_data['name'] = output_info['name']
            
            if 'isDefault' in output_info:
                audio_data['isDefault'] = output_info['isDefault']
            
            ref.set(audio_data)
            
            return True
            
        except Exception as e:
            print(f"Error updating audio output: {e}")
            return False
    
    def get_audio_output(
        self,
        user_id: str,
        device_id: str
    ) -> Optional[Dict]:
        """
        Get current audio output device information.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            
        Returns:
            Audio output info or None
        """
        if not user_id or not device_id:
            return None
        
        try:
            ref = db.reference(f'users/{user_id}/devices/{device_id}/audioOutput')
            audio_data = ref.get()
            
            if audio_data:
                return {
                    'type': audio_data.get('type'),
                    'name': audio_data.get('name'),
                    'isDefault': audio_data.get('isDefault'),
                    'timestamp': audio_data.get('timestamp')
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting audio output: {e}")
            return None
    
    def handle_output_change(
        self,
        user_id: str,
        device_id: str,
        old_output: str,
        new_output: str
    ) -> Dict:
        """
        Handle audio output device change event.
        
        Args:
            user_id: User's UID
            device_id: Device identifier
            old_output: Previous output type
            new_output: New output type
            
        Returns:
            Action recommendations
        """
        recommendations = {
            'pausePlayback': False,
            'adjustVolume': False,
            'showNotification': False,
            'message': ''
        }
        
        # Headphones disconnected -> pause playback
        if old_output == 'headphones' and new_output == 'speaker':
            recommendations['pausePlayback'] = True
            recommendations['showNotification'] = True
            recommendations['message'] = 'Headphones disconnected. Playback paused.'
        
        # Switched to headphones -> resume if was paused
        elif old_output == 'speaker' and new_output == 'headphones':
            recommendations['showNotification'] = True
            recommendations['message'] = 'Headphones connected.'
        
        # Bluetooth connected
        elif new_output == 'bluetooth':
            recommendations['showNotification'] = True
            recommendations['message'] = 'Bluetooth audio connected.'
        
        return recommendations


# Export singletons
network_monitor = NetworkMonitor()
audio_output_monitor = AudioOutputMonitor()
