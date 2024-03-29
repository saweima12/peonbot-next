from typing import Any

from .base import RedisBaseProxy

class RedisJsonProxy(RedisBaseProxy):

    async def set(self, obj: Any, path="."):
        await self.redis.json().set(self.namespace, path, obj)

    async def get(self, path="."):
        return await self.redis.json().get(self.namespace, path)

    async def exists_path(self, path="."):
        return (await self.type(path)) is not None

    async def type(self, path="."):
        return await self.redis.json().type(self.namespace, path)

    async def arrindex(self, value, path=".", **kwargs):
        return await self.redis.json().arrindex(self.namespace, path, value, **kwargs)
