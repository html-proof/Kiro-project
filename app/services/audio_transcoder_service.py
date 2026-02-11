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
    
    Args:
        source_url: Source audio URL (from YouTube)
        target_bitrate: Target bitrate (e.g., "64k", "128k")
    
    Yields:
        MP3 audio chunks in target bitrate
    """
    # FFmpeg command for MP3 output
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', source_url,           # Input URL
        '-vn',                       # No video
        '-acodec', 'libmp3lame',     # MP3 codec
        '-b:a', target_bitrate,      # Target bitrate
        '-f', 'mp3',                 # Output format
        '-',                         # Output to stdout
    ]
    
    logger.info(f"Starting FFmpeg MP3 transcode: {source_url} -> {target_bitrate}")
    
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
