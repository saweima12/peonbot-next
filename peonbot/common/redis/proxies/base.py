from abc import ABC
from redis.asyncio import Redis

class RedisBaseProxy(ABC):

    def __init__(self, namespace: str, connection: Redis):
        self.__redis = connection
        self.__namespace = namespace

    @property
    def redis(self):
        return self.__redis

    @property
    def namespace(self):
        return self.__namespace

    async def exists(self):
        return await self.__redis.exists(self.namespace)

    async def delete(self):
        return await self.__redis.delete(self.namespace)
