from redis.asyncio import ConnectionPool, StrictRedis
from .proxies import (
    RedisHashProxy,
    RedisJsonProxy
)

class RedisProxyFactory:

    def __init__(self, connection_pool: ConnectionPool):
        self.connection_pool = connection_pool

    def get_connection(self):
        return StrictRedis(connection_pool=self.connection_pool)

    def get_json(self, namespace: str, conn: StrictRedis) -> RedisJsonProxy:
        return RedisJsonProxy(namespace, conn)

    def get_hash_map(self, namespace: str, conn: StrictRedis) -> RedisHashProxy:
        return RedisHashProxy(namespace, conn)
