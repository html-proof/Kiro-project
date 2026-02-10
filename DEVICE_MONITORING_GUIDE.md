# Device Monitoring Guide

Complete guide for implementing audio output detection and network speed monitoring in your Musicly app.

## Features

### 1. Audio Output Detection
- Automatically detects headphones, speakers, and Bluetooth devices
- Pauses playback when headphones are disconnected
- Shows notifications on output device changes
- Tracks output preferences per device

### 2. Network Speed Monitoring
- Measures download speed in real-time
- Monitors latency
- Recommends optimal audio quality
- Adapts quality based on connection type (WiFi, cellular, etc.)

### 3. Device Management
- Registers and tracks all user devices
- Heartbeat monitoring to detect active devices
- Automatic cleanup of stale devices
- Multi-device playback control

## Backend API Endpoints

### Device Management

```
POST /device/register
  - Register a new device
  - Query: user_id, device_id
  - Body: { name, platform, userAgent }

GET /device/list
  - Get all devices for a user
  - Query: user_id

POST /device/heartbeat
  - Update device heartbeat
  - Query: user_id, device_id

DELETE /device/remove
  - Remove a device
  - Query: user_id, device_id
```

### Network Monitoring

```
POST /device/network/update
  - Update network speed
  - Query: user_id, device_id, speed_mbps, latency_ms

GET /device/network/info
  - Get network information
  - Query: user_id, device_id

GET /device/network/quality
  - Get adaptive quality recommendation
  - Query: user_id, device_id, requested_quality (optional)

POST /device/network/connection-type
  - Update connection type
  - Query: user_id, device_id, connection_type
```

### Audio Output

```
POST /device/audio/output
  - Update audio output device
  - Query: user_id, device_id
  - Body: { type, name, isDefault }

GET /device/audio/output
  - Get current audio output
  - Query: user_id, device_id

POST /device/audio/output-change
  - Handle output change event
  - Query: user_id, device_id, old_output, new_output
```

## Client-Side Integration

### JavaScript/Web

```javascript
import DeviceMonitor from './deviceMonitor.js';

// Initialize
const monitor = new DeviceMonitor(
  'https://your-api.com',
  'user_123',
  'device_456'
);

await monitor.initialize();

// Handle audio output changes
monitor.onAudioOutputChange = (recommendations) => {
  if (recommendations.pausePlayback) {
    player.pause();
  }
  
  if (recommendations.showNotification) {
    showNotification(recommendations.message);
  }
};

// Handle quality recommendations
monitor.onQualityRecommendation = (quality) => {
  player.setQuality(quality);
};

// Get adaptive quality
const quality = await monitor.getAdaptiveQuality('high');
player.setQuality(quality);

// Cleanup on unmount
monitor.destroy();
```

### React Native

```javascript
import { useEffect, useState } from 'react';
import NetInfo from '@react-native-community/netinfo';
import { Audio } from 'expo-av';

const useDeviceMonitor = (userId, deviceId) => {
  const [audioOutput, setAudioOutput] = useState('speaker');
  const [networkSpeed, setNetworkSpeed] = useState(null);

  useEffect(() => {
    // Register device
    registerDevice();

    // Monitor network
    const unsubscribe = NetInfo.addEventListener(state => {
      updateNetworkInfo(state);
    });

    // Monitor audio output
    const audioSubscription = Audio.addAudioModeListener(({ isHeadphonesConnected }) => {
      const newOutput = isHeadphonesConnected ? 'headphones' : 'speaker';
      handleAudioOutputChange(audioOutput, newOutput);
      setAudioOutput(newOutput);
    });

    return () => {
      unsubscribe();
      audioSubscription.remove();
    };
  }, []);

  const registerDevice = async () => {
    const deviceInfo = {
      name: await Device.getDeviceNameAsync(),
      platform: Platform.OS,
      userAgent: await Device.getDeviceTypeAsync()
    };

    await fetch(`${API_URL}/device/register?user_id=${userId}&device_id=${deviceId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(deviceInfo)
    });
  };

  const updateNetworkInfo = async (state) => {
    const speedMbps = estimateSpeed(state);
    setNetworkSpeed(speedMbps);

    await fetch(
      `${API_URL}/device/network/update?user_id=${userId}&device_id=${deviceId}&speed_mbps=${speedMbps}`,
      { method: 'POST' }
    );
  };

  const handleAudioOutputChange = async (oldOutput, newOutput) => {
    const response = await fetch(
      `${API_URL}/device/audio/output-change?user_id=${userId}&device_id=${deviceId}&old_output=${oldOutput}&new_output=${newOutput}`,
      { method: 'POST' }
    );

    const data = await response.json();
    
    if (data.data.pausePlayback) {
      // Pause playback
      player.pause();
    }
  };

  return { audioOutput, networkSpeed };
};
```

### Flutter

```dart
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:headset_connection_event/headset_connection_event.dart';

class DeviceMonitor {
  final String apiUrl;
  final String userId;
  final String deviceId;

  DeviceMonitor(this.apiUrl, this.userId, this.deviceId);

  Future<void> initialize() async {
    await registerDevice();
    startHeartbeat();
    setupAudioOutputDetection();
    setupNetworkMonitoring();
  }

  Future<void> registerDevice() async {
    final deviceInfo = {
      'name': await DeviceInfo().deviceName,
      'platform': Platform.operatingSystem,
      'userAgent': Platform.operatingSystemVersion,
    };

    await http.post(
      Uri.parse('$apiUrl/device/register?user_id=$userId&device_id=$deviceId'),
      body: jsonEncode(deviceInfo),
      headers: {'Content-Type': 'application/json'},
    );
  }

  void setupAudioOutputDetection() {
    HeadsetConnectionEvent().getCurrentState.then((val) {
      updateAudioOutput(val == HeadsetState.CONNECT ? 'headphones' : 'speaker');
    });

    HeadsetConnectionEvent().setListener((val) {
      final newOutput = val == HeadsetState.CONNECT ? 'headphones' : 'speaker';
      handleAudioOutputChange(newOutput);
    });
  }

  void setupNetworkMonitoring() {
    Connectivity().onConnectivityChanged.listen((result) {
      updateConnectionType(result.toString());
    });

    // Check speed periodically
    Timer.periodic(Duration(minutes: 5), (_) {
      checkNetworkSpeed();
    });
  }

  Future<void> updateAudioOutput(String outputType) async {
    await http.post(
      Uri.parse('$apiUrl/device/audio/output?user_id=$userId&device_id=$deviceId'),
      body: jsonEncode({'type': outputType}),
      headers: {'Content-Type': 'application/json'},
    );
  }
}
```

## Quality Thresholds

The system automatically recommends quality based on network speed:

| Speed (Mbps) | Quality | Bitrate |
|--------------|---------|---------|
| ≥ 2.0        | Ultra   | 320kbps |
| ≥ 1.0        | High    | 192kbps |
| ≥ 0.5        | Medium  | 128kbps |
| < 0.5        | Saver   | 64kbps  |

## Audio Output Types

- `headphones` - Wired headphones/earbuds
- `speaker` - Built-in or external speakers
- `bluetooth` - Bluetooth headphones/speakers
- `external` - Other external audio devices

## Best Practices

1. **Initialize Early**: Start device monitoring as soon as the app launches
2. **Handle Disconnects**: Always pause playback when headphones disconnect
3. **Adaptive Quality**: Use network-based quality recommendations
4. **Heartbeat**: Send heartbeat every 2 minutes to keep device active
5. **Cleanup**: Remove device monitoring when user logs out
6. **Notifications**: Show user-friendly messages on device changes

## Example: Complete Integration

```javascript
class MusicPlayer {
  constructor(userId, deviceId) {
    this.monitor = new DeviceMonitor(API_URL, userId, deviceId);
    this.player = new AudioPlayer();
    this.currentQuality = 'medium';
  }

  async initialize() {
    await this.monitor.initialize();

    // Handle audio output changes
    this.monitor.onAudioOutputChange = (recommendations) => {
      if (recommendations.pausePlayback) {
        this.player.pause();
        this.showNotification(recommendations.message);
      }
    };

    // Handle quality recommendations
    this.monitor.onQualityRecommendation = (quality) => {
      if (quality !== this.currentQuality) {
        this.currentQuality = quality;
        this.player.setQuality(quality);
        console.log(`Quality adjusted to ${quality}`);
      }
    };
  }

  async play(songId) {
    // Get adaptive quality
    const quality = await this.monitor.getAdaptiveQuality(this.currentQuality);
    
    // Fetch stream with recommended quality
    const stream = await this.fetchStream(songId, quality);
    
    // Play
    this.player.play(stream);
  }

  showNotification(message) {
    // Show toast/snackbar
    console.log('Notification:', message);
  }
}
```

## Troubleshooting

### Audio Output Not Detected
- Ensure browser has microphone permissions (needed for enumerateDevices)
- Check if MediaDevices API is supported
- Test with different browsers

### Network Speed Inaccurate
- Increase test file size for more accurate measurements
- Run multiple tests and average results
- Consider using dedicated speed test APIs

### Heartbeat Not Working
- Check network connectivity
- Verify API endpoint is accessible
- Ensure intervals are not cleared prematurely

## Security Considerations

1. **Device ID**: Use secure, unique device identifiers
2. **User ID**: Always validate user authentication
3. **Rate Limiting**: Implement rate limits on heartbeat endpoints
4. **Data Privacy**: Don't store sensitive device information

## Performance Tips

1. **Debounce**: Debounce network checks to avoid excessive API calls
2. **Cache**: Cache network info for 5 minutes
3. **Background**: Run monitoring in background threads
4. **Battery**: Adjust check frequency based on battery level
