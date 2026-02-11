"""
Keepalive script to prevent Railway container from sleeping
Pings the /ping endpoint every 5 minutes
"""
import asyncio
import httpx
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def keepalive():
    """Ping the server every 5 minutes to keep it alive"""
    # Get the port from environment or use default
    port = os.environ.get("PORT", "8000")
    url = f"http://0.0.0.0:{port}/ping"
    
    # Wait longer for server to be fully ready
    logger.info("Keepalive: Waiting 60 seconds for server to start...")
    await asyncio.sleep(60)
    
    consecutive_failures = 0
    max_failures = 3
    
    while True:
        try:
            await asyncio.sleep(300)  # Wait 5 minutes
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    logger.info(f"✅ Keepalive ping successful at {datetime.now()}")
                    consecutive_failures = 0  # Reset on success
                else:
                    consecutive_failures += 1
                    logger.warning(f"⚠️ Keepalive ping returned {response.status_code} (failures: {consecutive_failures})")
        except Exception as e:
            consecutive_failures += 1
            logger.error(f"❌ Keepalive ping failed: {e} (failures: {consecutive_failures})")
            
            # If too many consecutive failures, the server might be down
            # Don't exit - just keep trying
            if consecutive_failures >= max_failures:
                logger.error(f"⚠️ {max_failures} consecutive failures - server may be down, but continuing...")
                consecutive_failures = 0  # Reset to avoid spam

if __name__ == "__main__":
    asyncio.run(keepalive())
