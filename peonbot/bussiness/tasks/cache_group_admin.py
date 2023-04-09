from aiogram import Bot
from redis.asyncio import Redis

from peonbot.common.scheduler import AbstractTask

class CacheGroupAdminTask(AbstractTask):

    def __init__(self, bot: Bot, redis: Redis):
        self.bot = bot
        self.redis = redis

    async def run(self):
        print(self.bot)
    