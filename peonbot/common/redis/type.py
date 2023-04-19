from redis.asyncio import ConnectionPool, Redis
from .proxies import (
    RedisHashProxy,
    RedisJsonProxy,
    RedisSetProxy
)

class RedisProxyFactory:

    def __init__(self, connection_pool: ConnectionPool):
        self.connection_pool = connection_pool

    def get_connection(self):
        return Redis(connection_pool=self.connection_pool, decode_responses=True)

    def get_json(self, namespace: str, conn: Redis) -> RedisJsonProxy:
        return RedisJsonProxy(namespace, conn)

    def get_hash_map(self, namespace: str, conn: Redis) -> RedisHashProxy:
        return RedisHashProxy(namespace, conn)

    def get_set(self, namespace: str, conn: Redis) -> RedisSetProxy:
        return RedisSetProxy(namespace, conn)
