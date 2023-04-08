from aiogram import Bot
from redis.asyncio import StrictRedis

from peonbot.common.scheduler import AbstractTask

class CacheGroupAdminTask(AbstractTask):

    def __init__(self, bot: Bot, redis: StrictRedis):
        self.bot = bot
        self.redis = redis

    async def run(self):
        print(self.bot)
    