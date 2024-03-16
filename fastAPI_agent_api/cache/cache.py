from redis.asyncio import Redis
from contextlib import asynccontextmanager
from env import REDIS_HOST, REDIS_PORT


@asynccontextmanager
async def redis_connection():
    client = await Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()
