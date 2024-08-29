import aioredis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_redis_value(key: str):
    return await redis.get(key)

async def set_redis_value(key: str, value: str):
    await redis.set(key, value)
