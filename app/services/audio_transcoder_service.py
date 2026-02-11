"""
Audio transcoding service - converts audio streams to 64kbps for bandwidth optimization
"""
import subprocess
import asyncio
import logging
from typing import AsyncIterator

logger = logging.getLogger(__name__)

async def transcode_audio_stream(source_url: str, target_bitrate: str = "64k") -> AsyncIterator[bytes]:
    """
    Transcode audio stream to target bitrate using FFmpeg
    
    Args:
        source_url: Source audio URL (from YouTube)
        target_bitrate: Target bitrate (e.g., "64k", "128k")
    
    Yields:
        Audio chunks in target bitrate
    """
    # FFmpeg command to transcode audio
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', source_url,           # Input URL
        '-vn',                       # No video
        '-acodec', 'libopus',        # Opus codec (best for low bitrate)
        '-b:a', target_bitrate,      # Target bitrate
        '-f', 'opus',                # Output format
        '-',                         # Output to stdout
    ]
    
    logger.info(f"Starting FFmpeg transcode: {source_url} -> {target_bitrate}")
    
    try:
        # Start FFmpeg process
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Stream output chunks
        chunk_size = 8192
        while True:
            chunk = await process.stdout.read(chunk_size)
            if not chunk:
                break
            yield chunk
        
        # Wait for process to complete
        await process.wait()
        
        if process.returncode != 0:
            stderr = await process.stderr.read()
            logger.error(f"FFmpeg error: {stderr.decode()}")
            
    except Exception as e:
        logger.error(f"Transcoding error: {e}")
        raise


async def transcode_audio_stream_mp3(source_url: str, target_bitrate: str = "64k") -> AsyncIterator[bytes]:
    """
    Transcode audio stream to MP3 format at target bitrate
    Optimized for instant playback with minimal latency
    
    Args:
        source_url: Source audio URL (from YouTube)
        target_bitrate: Target bitrate (e.g., "48k", "64k", "128k")
    
    Yields:
        MP3 audio chunks in target bitrate
    """
    # FFmpeg command for MP3 output with low-latency optimizations
    ffmpeg_cmd = [
        'ffmpeg',
        '-reconnect', '1',           # Auto-reconnect on network issues
        '-reconnect_streamed', '1',  # Reconnect for streamed content
        '-reconnect_delay_max', '2', # Max 2s reconnect delay
        '-i', source_url,            # Input URL
        '-vn',                       # No video
        '-acodec', 'libmp3lame',     # MP3 codec
        '-b:a', target_bitrate,      # Target bitrate
        '-q:a', '9',                 # Quality (9 = fastest encoding, lower quality)
        '-compression_level', '0',   # Fastest compression
        '-ar', '44100',              # Sample rate (44.1kHz)
        '-ac', '2',                  # Stereo
        '-f', 'mp3',                 # Output format
        '-fflags', '+nobuffer',      # No buffering for instant start
        '-flags', 'low_delay',       # Low delay mode
        '-',                         # Output to stdout
    ]
    
    logger.info(f"Starting FFmpeg MP3 transcode: {source_url} -> {target_bitrate} (low-latency mode)")
    
    try:
        # Start FFmpeg process
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Stream output chunks - smaller chunks for faster initial response
        chunk_size = 4096  # 4KB chunks for instant streaming
        while True:
            chunk = await process.stdout.read(chunk_size)
            if not chunk:
                break
            yield chunk
        
        # Wait for process to complete
        await process.wait()
        
        if process.returncode != 0:
            stderr = await process.stderr.read()
            logger.error(f"FFmpeg error: {stderr.decode()}")
            
    except Exception as e:
        logger.error(f"Transcoding error: {e}")
        raise
