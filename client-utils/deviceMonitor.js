/**
 * Client-side Device Monitoring Utilities
 * 
 * Features:
 * - Audio output detection (headphones/speaker)
 * - Network speed monitoring
 * - Automatic quality adjustment
 * - Device heartbeat
 */

class DeviceMonitor {
  constructor(apiBaseUrl, userId, deviceId) {
    this.apiBaseUrl = apiBaseUrl;
    this.userId = userId;
    this.deviceId = deviceId;
    this.audioContext = null;
    this.heartbeatInterval = null;
    this.networkCheckInterval = null;
  }

  /**
   * Initialize all monitoring features
   */
  async initialize() {
    await this.registerDevice();
    this.startHeartbeat();
    this.setupAudioOutputDetection();
    this.startNetworkMonitoring();
    this.setupConnectionTypeDetection();
  }

  /**
   * Register device with backend
   */
  async registerDevice() {
    try {
      const deviceInfo = {
        name: this.getDeviceName(),
        platform: this.getPlatform(),
        userAgent: navigator.userAgent
      };

      const response = await fetch(
        `${this.apiBaseUrl}/device/register?user_id=${this.userId}&device_id=${this.deviceId}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(deviceInfo)
        }
      );

      const data = await response.json();
      console.log('Device registered:', data);
    } catch (error) {
      console.error('Failed to register device:', error);
    }
  }

  /**
   * Start heartbeat to keep device alive
   */
  startHeartbeat() {
    // Send heartbeat every 2 minutes
    this.heartbeatInterval = setInterval(async () => {
      try {
        await fetch(
          `${this.apiBaseUrl}/device/heartbeat?user_id=${this.userId}&device_id=${this.deviceId}`,
          { method: 'POST' }
        );
      } catch (error) {
        console.error('Heartbeat failed:', error);
      }
    }, 120000); // 2 minutes
  }

  /**
   * Setup audio output detection
   */
  setupAudioOutputDetection() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
      console.warn('Audio output detection not supported');
      return;
    }

    // Initial detection
    this.detectAudioOutput();

    // Listen for device changes
    navigator.mediaDevices.addEventListener('devicechange', () => {
      this.detectAudioOutput();
    });
  }

  /**
   * Detect current audio output device
   */
  async detectAudioOutput() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const audioOutputs = devices.filter(device => device.kind === 'audiooutput');

      let outputType = 'speaker';
      let outputName = 'Default';

      // Check for headphones/bluetooth
      for (const device of audioOutputs) {
        const label = device.label.toLowerCase();
        
        if (label.includes('headphone') || label.includes('headset')) {
          outputType = 'headphones';
          outputName = device.label;
          break;
        } else if (label.includes('bluetooth')) {
          outputType = 'bluetooth';
          outputName = device.label;
          break;
        }
      }

      // Update backend
      await this.updateAudioOutput({
        type: outputType,
        name: outputName,
        isDefault: audioOutputs.length > 0 && audioOutputs[0].deviceId === 'default'
      });

      console.log('Audio output detected:', outputType, outputName);
    } catch (error) {
      console.error('Failed to detect audio output:', error);
    }
  }

  /**
   * Update audio output in backend
   */
  async updateAudioOutput(outputInfo) {
    try {
      const response = await fetch(
        `${this.apiBaseUrl}/device/audio/output?user_id=${this.userId}&device_id=${this.deviceId}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(outputInfo)
        }
      );

      const data = await response.json();
      
      // Handle recommendations (e.g., pause on headphone disconnect)
      if (data.data && data.data.pausePlayback) {
        this.onAudioOutputChange(data.data);
      }
    } catch (error) {
      console.error('Failed to update audio output:', error);
    }
  }

  /**
   * Start network speed monitoring
   */
  startNetworkMonitoring() {
    // Check network speed every 5 minutes
    this.checkNetworkSpeed();
    this.networkCheckInterval = setInterval(() => {
      this.checkNetworkSpeed();
    }, 300000); // 5 minutes
  }

  /**
   * Check network speed using download test
   */
  async checkNetworkSpeed() {
    try {
      // Use a small test file (1MB)
      const testUrl = `${this.apiBaseUrl}/ping?t=${Date.now()}`;
      const startTime = performance.now();
      
      const response = await fetch(testUrl);
      await response.blob();
      
      const endTime = performance.now();
      const duration = (endTime - startTime) / 1000; // seconds
      const fileSizeBytes = 1024; // Approximate response size
      const speedMbps = (fileSizeBytes * 8) / (duration * 1000000);

      // Get latency
      const latencyStart = performance.now();
      await fetch(testUrl, { method: 'HEAD' });
      const latency = performance.now() - latencyStart;

      // Update backend
      await this.updateNetworkSpeed(speedMbps, latency);

      console.log(`Network speed: ${speedMbps.toFixed(2)} Mbps, Latency: ${latency.toFixed(0)} ms`);
    } catch (error) {
      console.error('Failed to check network speed:', error);
    }
  }

  /**
   * Update network speed in backend
   */
  async updateNetworkSpeed(speedMbps, latencyMs) {
    try {
      const response = await fetch(
        `${this.apiBaseUrl}/device/network/update?user_id=${this.userId}&device_id=${this.deviceId}&speed_mbps=${speedMbps}&latency_ms=${latencyMs}`,
        { method: 'POST' }
      );

      const data = await response.json();
      
      if (data.data && data.data.recommended_quality) {
        this.onQualityRecommendation(data.data.recommended_quality);
      }
    } catch (error) {
      console.error('Failed to update network speed:', error);
    }
  }

  /**
   * Setup connection type detection
   */
  setupConnectionTypeDetection() {
    if ('connection' in navigator) {
      const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      
      if (connection) {
        // Initial detection
        this.updateConnectionType(connection.effectiveType);

        // Listen for changes
        connection.addEventListener('change', () => {
          this.updateConnectionType(connection.effectiveType);
        });
      }
    }
  }

  /**
   * Update connection type in backend
   */
  async updateConnectionType(connectionType) {
    try {
      await fetch(
        `${this.apiBaseUrl}/device/network/connection-type?user_id=${this.userId}&device_id=${this.deviceId}&connection_type=${connectionType}`,
        { method: 'POST' }
      );

      console.log('Connection type:', connectionType);
    } catch (error) {
      console.error('Failed to update connection type:', error);
    }
  }

  /**
   * Get adaptive quality recommendation
   */
  async getAdaptiveQuality(requestedQuality = null) {
    try {
      let url = `${this.apiBaseUrl}/device/network/quality?user_id=${this.userId}&device_id=${this.deviceId}`;
      if (requestedQuality) {
        url += `&requested_quality=${requestedQuality}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      return data.data.quality;
    } catch (error) {
      console.error('Failed to get adaptive quality:', error);
      return 'medium';
    }
  }

  /**
   * Helper: Get device name
   */
  getDeviceName() {
    const ua = navigator.userAgent;
    
    if (/iPhone/.test(ua)) return 'iPhone';
    if (/iPad/.test(ua)) return 'iPad';
    if (/Android/.test(ua)) return 'Android Device';
    if (/Windows/.test(ua)) return 'Windows PC';
    if (/Mac/.test(ua)) return 'Mac';
    if (/Linux/.test(ua)) return 'Linux PC';
    
    return 'Unknown Device';
  }

  /**
   * Helper: Get platform
   */
  getPlatform() {
    const ua = navigator.userAgent;
    
    if (/iPhone|iPad|iPod/.test(ua)) return 'ios';
    if (/Android/.test(ua)) return 'android';
    if (/Windows/.test(ua)) return 'windows';
    if (/Mac/.test(ua)) return 'macos';
    if (/Linux/.test(ua)) return 'linux';
    
    return 'web';
  }

  /**
   * Callback: Audio output changed
   * Override this in your app to handle output changes
   */
  onAudioOutputChange(recommendations) {
    console.log('Audio output changed:', recommendations);
    
    if (recommendations.pausePlayback) {
      // Pause playback
      console.log('Pausing playback due to output change');
    }
    
    if (recommendations.showNotification) {
      // Show notification
      console.log('Notification:', recommendations.message);
    }
  }

  /**
   * Callback: Quality recommendation changed
   * Override this in your app to adjust quality
   */
  onQualityRecommendation(quality) {
    console.log('Recommended quality:', quality);
  }

  /**
   * Cleanup
   */
  destroy() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }
    
    if (this.networkCheckInterval) {
      clearInterval(this.networkCheckInterval);
    }
  }
}

// Export for use in apps
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DeviceMonitor;
}
