from typing import Awaitable
from asyncio import Task, Future
from sanic import Sanic
from peonbot.bussiness.repositories import BotContextRepository

class CommonService:

    def __init__(self, app: Sanic, bot_repo: BotContextRepository):
        self.app = app
        self.bot_repo = bot_repo

    async def get_whitelist(self):
        return await self.bot_repo.get_whitelist()

    async def is_whitelist(self, user_id: str):
        whitelist = await self.bot_repo.get_whitelist()
        return user_id in whitelist

    async def get_delete_cache(self, chat_id: str, user_id: str) -> int:
        return await self.bot_repo.get_delete_cache(chat_id, user_id)

    async def set_delete_cache(self, chat_id: str, user_id: str) -> int:
        return await self.bot_repo.set_delete_cache(chat_id, user_id)

    async def record_delete_message(self, chat_id: str, content_type: str, data: dict):
        await self.bot_repo.record_deleted_message(chat_id, content_type, data)

    def add_task(self, task: Task | Future | Awaitable):
        self.app.add_task(task)
