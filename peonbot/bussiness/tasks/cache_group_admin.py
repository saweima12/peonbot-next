import traceback
from aiogram import Bot
from sanic.log import logger

from peonbot.common.redis import RedisProxyFactory
from peonbot.common.scheduler import AbstractTask
from peonbot.bussiness.repositories import ChatConfigRepository


class CacheGroupAdminTask(AbstractTask):

    def __init__(self, bot: Bot, redis_factory: RedisProxyFactory):
        self.bot = bot
        # initialize repository & service
        self.chat_repo = ChatConfigRepository(redis_factory)

    async def run(self):

        chat_ids = await self.chat_repo.get_avaliable_chat_ids()

        for chat_id in chat_ids:
            try:
                admin_list = await self.bot.get_chat_administrators(chat_id)
                admin_ids = [str(admin.user.id) for admin in admin_list]

                config = await self.chat_repo.get_config(chat_id)
                config.adminstrators = admin_ids

                await self.chat_repo.set_config_cache(chat_id, config)
            except Exception:
                logger.error(traceback.format_exc())
