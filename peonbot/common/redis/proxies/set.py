from typing import Set
from .base import RedisBaseProxy

class RedisSetProxy(RedisBaseProxy):

    async def members(self) -> Set:
        return await self.redis.smembers(self.namespace)

    async def exists_item(self, value: str) -> int:
        return await self.redis.sismember(self.namespace, value)

    async def add(self, *values) -> int:
        return await self.redis.sadd(self.namespace, *values)

    async def delete_item(self, value: str) -> int:
        return await self.redis.srem(self.namespace, value)
