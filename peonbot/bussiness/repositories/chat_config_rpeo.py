from sanic.log import logger

from peonbot.models.db import PeonChatConfig
from peonbot.models.redis import ChatConfig
from .base import BaseRepository

class ChatConfigRepository(BaseRepository):

    async def get_config(self, chat_id: str) -> ChatConfig | None:
        # generate namespace string.
        namespace = self.get_namespace(chat_id)
        logger.debug(f"Query namespace: {namespace}")
        async with self.redis_conn() as conn:
            # create proxy
            proxy = self.factory.get_json(namespace, conn)
            # get data.
            result = await proxy.get()

            if result:
                return ChatConfig(**result)

        # try get data from database.
        result = await PeonChatConfig.get_or_none(chat_id=chat_id)
        if result:
            # found config from dataase.
            data = ChatConfig(**result.config_json)
            # save to redis cache.
            await self.set_cache(chat_id, data)
            return data

        return None

    async def set_cache(self, chat_id: str, data: ChatConfig):
        # generate namespace string.
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_json(namespace, conn)
            await proxy.set(data.dict())


    async def set_db(self, chat_id: str, data: ChatConfig):
        # write into database.
        await PeonChatConfig.update_or_create({
            'status': data.status,
            'chat_name': data.chat_name,
            'config_json': data.dict()
        }, chat_id=chat_id)


    def get_namespace(self, chat_id: str):
        return f"{chat_id}:config"
