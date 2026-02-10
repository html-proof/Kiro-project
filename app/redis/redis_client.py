import redis
from app.config import settings

redis_client = None

def initialize_redis():
    global redis_client
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)

def get_redis():
    return redis_client
