from typing import Set
from datetime import timedelta

from sanic.log import logger

from peonbot.models.db import PeonUserWhitelist, PeonDeletedMessage

from .base import BaseRepository


class BotContextRepository(BaseRepository):

    async def get_whitelist(self) -> Set[str]:
        namespace = self.get_namespace("whitelist")

        async with self.redis_conn() as conn:
            proxy = self.factory.get_set(namespace, conn)
            logger.debug(f"Query namespace: {namespace}")

            result = await proxy.members()
            result = [ item.decode("utf-8") for item in list(result)]
            if result:
                return set(result)

            result = await PeonUserWhitelist.all()
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

    async def get_delete_cache(self, chat_id: str, user_id: str) -> int | None:
        namespace = self.get_namespace(f"deleted:{chat_id}:{user_id}")
        async with self.redis_conn() as conn:
            result = await conn.get(namespace)
            if result:
                return int(result)
        return None



    async def set_delete_cache(self, chat_id: str, user_id: str) -> int:
        namespace = self.get_namespace(f"deleted:{chat_id}:{user_id}")

        async with self.redis_conn() as conn:
            result = await conn.set(namespace, "1", ex=timedelta(seconds=60), nx=True)
            if result:
                return 1

            return await conn.incr(namespace)
    
    async def record_deleted_message(self, chat_id: str, content_type: str, data: dict):
        await PeonDeletedMessage.create(chat_id=chat_id,
                                content_type=content_type,
                                message_json=data)

    def get_namespace(self, key: str) -> str:
        return f"bot:{key}"
