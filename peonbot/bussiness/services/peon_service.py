import asyncio
import traceback
from sanic import Sanic
from sanic.log import logger

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from peonbot.bussiness.repositories import BotContextRepository

class PeonService:

    def __init__(self, bot: Bot, bot_repo: BotContextRepository, app: Sanic):
        self.bot = bot
        self.bot_repo = bot_repo
        self.app = app

    async def is_whitelist(self, user_id: str):
        whitelist = await self.bot_repo.get_whitelist()
        return user_id.encode("utf-8") in whitelist

    async def delete_message(self, chat_id: str, message_id: str) -> bool:
        for _ in range(3):
            is_success = await self._delete_message(chat_id, message_id)

            if is_success:
                return True

            await asyncio.sleep(1)
        return False

    async def send_delete_message(self, chat_id: str, user_id: str, text: str) -> Message | None:
        is_success = await self.bot_repo.set_delete_record(chat_id, user_id)

        if not is_success:
            return

        try:
            message = await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='markdown')
            _task = self._deleay_delete_message(chat_id, str(message.message_id))
            self.app.add_task(_task)

        except Exception:
            return None

    async def _deleay_delete_message(self, chat_id: str, message_id: str):
        await asyncio.sleep(30)
        await self.delete_message(chat_id, message_id)

    async def _delete_message(self, chat_id: str, message_id: str) -> bool:
        try:
            await self.bot.delete_message(chat_id, message_id)
            return True
        except MessageToDeleteNotFound:
            return True
        except Exception as _e:
            logger.error(traceback.format_exc())
            return False
