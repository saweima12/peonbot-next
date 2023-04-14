from peonbot.common.redis import RedisProxyFactory
from peonbot.common.scheduler import AbstractTask
from peonbot.bussiness.repositories import (
    BotContextRepository,
    ChatConfigRepository,
    RecordRepository
)

from peonbot.models.db import (
    PeonChatConfig
)


class CacheToDBTask(AbstractTask):

    def __init__(self, redis_factory: RedisProxyFactory):
        self.chat_repo = ChatConfigRepository(redis_factory)
        self.record_repo = RecordRepository(redis_factory)
        self.bot_repo = BotContextRepository(redis_factory)

    async def run(self):
        # save user whitelist
        whitelist = await self.bot_repo.get_whitelist()
        await self.bot_repo.set_whitelist_db(whitelist)

        # save chat config to database.
        chats = await PeonChatConfig.filter(status="ok")

        for chat in chats:
            # save chat config
            config_cache = await self.chat_repo.get_config(chat.chat_id)
            await self.chat_repo.set_config_db(chat.chat_id, config_cache)

            # save user record
            user_records = await self.record_repo.get_record_cache(chat.chat_id)
            for data in user_records.values():
                await self.record_repo.set_db(chat.chat_id, data)
            await self.record_repo.clean_cache(chat.chat_id)
            