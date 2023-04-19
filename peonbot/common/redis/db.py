from sanic import Sanic
from sanic.log import logger
from redis.asyncio import ConnectionPool, Redis
from .type import RedisProxyFactory

SERVICE_CODE = "redis"

def get_conn(app: Sanic) -> Redis:
    _pool = get_pool(app)
    return Redis(connection_pool=_pool)

def get_factory(app: Sanic) -> RedisProxyFactory:
    _pool = get_pool(app)
    return RedisProxyFactory(connection_pool=_pool)

def get_pool(app: Sanic) -> ConnectionPool:
    if not hasattr(app.ctx, SERVICE_CODE):
        logger.error(f"{SERVICE_CODE} not found.")
        return None
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic):
    redis_uri = app.config["REDIS_URI"]
    pool = ConnectionPool.from_url(redis_uri)

    @app.before_server_stop
    async def dispose(_):
        if hasattr(app.ctx, SERVICE_CODE):
            await pool.disconnect()

    setattr(app.ctx, SERVICE_CODE, pool)
    logger.info(f"Register redis connection pool: {SERVICE_CODE}")
    return pool
