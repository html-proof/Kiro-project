import json
from app.redis.redis_client import get_redis

def cache_set(key: str, value: any, ttl: int = 300):
    redis = get_redis()
    redis.setex(key, ttl, json.dumps(value))

def cache_get(key: str):
    redis = get_redis()
    data = redis.get(key)
    return json.loads(data) if data else None

def cache_delete(key: str):
    redis = get_redis()
    redis.delete(key)
