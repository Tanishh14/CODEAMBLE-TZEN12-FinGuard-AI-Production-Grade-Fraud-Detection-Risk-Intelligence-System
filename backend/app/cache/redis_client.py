"""Redis client stub. Replace with aioredis or redis-py in production."""
import logging

log = logging.getLogger("finguard.cache")


class RedisClient:
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self.url = url

    async def connect(self):
        log.info("Redis connect stub: %s", self.url)

    async def close(self):
        log.info("Redis close stub")

    async def get(self, key: str):
        return None

    async def set(self, key: str, value, expire: int = None):
        log.info("Redis set stub %s", key)


redis_client = RedisClient()
