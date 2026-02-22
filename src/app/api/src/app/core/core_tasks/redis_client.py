from __future__ import annotations

from typing import Optional

from redis.asyncio import Redis

from app.config import get_redis_settings

_redis_client: Optional[Redis] = None


def get_redis_client() -> Redis:
    """Return a singleton Redis client configured from environment.

    Raises a :class:`RuntimeError` if the REDIS_URL setting is missing.
    """
    global _redis_client
    if _redis_client is None:
        settings = get_redis_settings()
        url = settings.REDIS_URL
        if not url:
            raise RuntimeError("REDIS_URL must be set to connect to Redis")
        # redis-py >=4 exposes ``Redis.from_url`` to create clients
        _redis_client = Redis.from_url(url)
    return _redis_client
