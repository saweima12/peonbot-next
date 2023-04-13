from typing import Set
from datetime import timedelta

from sanic.log import logger

from peonbot.models.db import PeonUserWhitelist

from .base import BaseRepository


class BotContextRepository(BaseRepository):

    async def get_whitelist(self) -> Set[str]:
        namespace = self.get_namespace("whitelist")

        async with self.redis_conn() as conn:
            proxy = self.factory.get_set(namespace, conn)
            logger.debug(f"Query namespace: {namespace}")

            result = await proxy.members()
            if result:
                return set(result)

            result = await PeonUserWhitelist.all()
            print(result)
            if result:
                user_ids = [item.user_id for item in result]
                await proxy.add(*user_ids)
                return set(user_ids)

        return set()

    async def set_whitelist_cache(self, *values):
        namespace = self.get_namespace("whitelist")

        async with self.redis_conn() as conn:
            proxy = self.factory.get_set(namespace, conn)
            await proxy.delete()
            await proxy.add(*values)


    async def set_whitelist_db(self, user_ids: Set[str]):
        for user_id in list(user_ids):
            await PeonUserWhitelist.update_or_create({
                "status": "ok"
            }, user_id=user_id)

    async def set_delete_record(self, chat_id: str, user_id: str) -> bool:
        namespace = self.get_namespace(f"deleted:{chat_id}:{user_id}")

        async with self.redis_conn() as conn:
            result = await conn.set(namespace, "test", ex=timedelta(seconds=60), nx=True)
            if result:
                return True
        return False

    def get_namespace(self, key: str) -> str:
        return f"bot:{key}"
