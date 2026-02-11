"""
Keepalive script to prevent Railway container from sleeping
Pings the /ping endpoint every 5 minutes
"""
import asyncio
import httpx
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def keepalive():
    """Ping the server every 5 minutes to keep it alive"""
    url = "http://localhost:8000/ping"
    
    while True:
        try:
            await asyncio.sleep(300)  # Wait 5 minutes
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    logger.info(f"✅ Keepalive ping successful at {datetime.now()}")
                else:
                    logger.warning(f"⚠️ Keepalive ping returned {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Keepalive ping failed: {e}")

if __name__ == "__main__":
    asyncio.run(keepalive())
