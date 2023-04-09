from aiogram import Bot
from peonbot.bussiness.repositories import BotConfigRepository


class PeonService:

    def __init__(self, bot: Bot, bot_repo: BotConfigRepository):
        self.bot = bot
        self.bot_repo = bot_repo

    async def is_whitelist(self, user_id: str):
        whitelist = await self.bot_repo.get_whitelist()
        return user_id.encode("utf-8") in whitelist
