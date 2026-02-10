import redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)
redis_client = None

def initialize_redis():
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        # Test connection
        redis_client.ping()
        logger.info("✅ Redis connected successfully")
    except Exception as e:
        logger.warning(f"⚠️ Redis connection failed: {e}. Continuing without Redis cache.")
        redis_client = None

def get_redis():
    return redis_client
