import redis.asyncio as redis
import os
from dotenv import load_dotenv
import asyncio
from utils.logger import logger
from typing import List, Any
from utils.retry import retry
from urllib.parse import urlparse

# Redis client and connection pool
client: redis.Redis | None = None
pool: redis.ConnectionPool | None = None
_initialized = False
_init_lock = asyncio.Lock()

# Constants
REDIS_KEY_TTL = 3600 * 24  # 24 hour TTL as safety mechanism


def initialize():
    """Initialize Redis connection pool and client using environment variables."""
    global client, pool

    # Load environment variables if not already loaded
    load_dotenv()

    # Check if REDIS_URL is provided (common in cloud deployments)
    redis_url = os.getenv("REDIS_URL")
    
    if redis_url:
        # Parse Redis URL (e.g., redis://user:pass@host:port/db or rediss://... for SSL)
        parsed = urlparse(redis_url)
        redis_host = parsed.hostname or "redis"
        redis_port = parsed.port or 6379
        redis_password = parsed.password or ""
        redis_ssl = parsed.scheme == "rediss"
        redis_db = int(parsed.path.lstrip('/')) if parsed.path and parsed.path != '/' else 0
        
        logger.info(f"Using REDIS_URL for connection to {redis_host}:{redis_port} (SSL: {redis_ssl})")
    else:
        # Fallback to individual environment variables
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_password = os.getenv("REDIS_PASSWORD", "")
        # Convert string 'True'/'False' to boolean
        redis_ssl_str = os.getenv("REDIS_SSL", "False")
        redis_ssl = redis_ssl_str.lower() == "true"
        redis_db = 0
        
        logger.info(f"Using individual Redis env vars for connection to {redis_host}:{redis_port}")
    
    # Connection pool configuration
    max_connections = int(os.getenv("REDIS_MAX_CONNECTIONS", 1024))
    retry_on_timeout = not (os.getenv("REDIS_RETRY_ON_TIMEOUT", "True").lower() != "true")

    logger.info(f"Initializing Redis connection pool to {redis_host}:{redis_port} with max {max_connections} connections")

    # Create connection pool
    pool_kwargs = {
        "host": redis_host,
        "port": redis_port,
        "password": redis_password,
        "db": redis_db,
        "decode_responses": True,
        "socket_timeout": 5.0,
        "socket_connect_timeout": 5.0,
        "retry_on_timeout": retry_on_timeout,
        "health_check_interval": 30,
        "max_connections": max_connections,
    }
    
    # Only add SSL parameter if SSL is enabled
    if redis_ssl:
        pool_kwargs["ssl"] = True
    
    pool = redis.ConnectionPool(**pool_kwargs)

    # Create Redis client from connection pool
    client = redis.Redis(connection_pool=pool)

    return client


async def initialize_async():
    """Initialize Redis connection asynchronously."""
    global client, _initialized

    async with _init_lock:
        if not _initialized:
            logger.info("Initializing Redis connection")
            initialize()

        try:
            await client.ping()
            logger.info("Successfully connected to Redis")
            _initialized = True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            client = None
            _initialized = False
            raise

    return client


async def close():
    """Close Redis connection and connection pool."""
    global client, pool, _initialized
    if client:
        logger.info("Closing Redis connection")
        await client.aclose()
        client = None
    
    if pool:
        logger.info("Closing Redis connection pool")
        await pool.aclose()
        pool = None
    
    _initialized = False
    logger.info("Redis connection and pool closed")


async def get_client():
    """Get the Redis client, initializing if necessary."""
    global client, _initialized
    if client is None or not _initialized:
        await retry(lambda: initialize_async())
    return client


# Basic Redis operations
async def set(key: str, value: str, ex: int = None, nx: bool = False):
    """Set a Redis key."""
    redis_client = await get_client()
    return await redis_client.set(key, value, ex=ex, nx=nx)


async def get(key: str, default: str = None):
    """Get a Redis key."""
    redis_client = await get_client()
    result = await redis_client.get(key)
    return result if result is not None else default


async def delete(key: str):
    """Delete a Redis key."""
    redis_client = await get_client()
    return await redis_client.delete(key)


async def publish(channel: str, message: str):
    """Publish a message to a Redis channel."""
    redis_client = await get_client()
    return await redis_client.publish(channel, message)


async def create_pubsub():
    """Create a Redis pubsub object."""
    redis_client = await get_client()
    return redis_client.pubsub()


# List operations
async def rpush(key: str, *values: Any):
    """Append one or more values to a list."""
    redis_client = await get_client()
    return await redis_client.rpush(key, *values)


async def lrange(key: str, start: int, end: int) -> List[str]:
    """Get a range of elements from a list."""
    redis_client = await get_client()
    return await redis_client.lrange(key, start, end)


async def llen(key: str) -> int:
    """Get the length of a list."""
    redis_client = await get_client()
    return await redis_client.llen(key)


# Key management
async def expire(key: str, time: int):
    """Set a key's time to live in seconds."""
    redis_client = await get_client()
    return await redis_client.expire(key, time)


async def keys(pattern: str) -> List[str]:
    """Get keys matching a pattern."""
    redis_client = await get_client()
    return await redis_client.keys(pattern)
