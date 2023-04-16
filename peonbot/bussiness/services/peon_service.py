import asyncio
import traceback
from datetime import timedelta
from sanic.log import logger

from aiogram import Bot
from aiogram.types import Message, ChatPermissions
from aiogram.utils.exceptions import MessageToDeleteNotFound

from peonbot.models.common import PermissionLevel
from peonbot.bussiness.services import CommonService, RecordService

class PeonService:

    def __init__(self, bot: Bot, common_service: CommonService, record_service: RecordService):
        self.bot = bot
        self.common_service = common_service
        self.record_service = record_service

    async def set_member_permission(self,
                                    chat_id: str,
                                    user_id: str,
                                    level: PermissionLevel,
                                    until_date: timedelta = None):
        if level == PermissionLevel.ALLOW:
            permission = ChatPermissions(can_send_messages=True,
                                    can_send_media_messages=True,
                                    can_send_other_messages=True,
                                    can_add_web_page_previews=True)
        elif level == PermissionLevel.LIMIT:
            permission = ChatPermissions(can_send_messages=True,
                                    can_send_media_messages=False,
                                    can_send_other_messages=False,
                                    can_add_web_page_previews=False)
        else:
            permission = ChatPermissions(can_send_messages=False,
                                    can_send_media_messages=False,
                                    can_send_other_messages=False,
                                    can_add_web_page_previews=False)

        return await self.bot.restrict_chat_member(chat_id, user_id, permissions=permission, until_date=until_date)


    async def delete_message(self, chat_id: str, message_id: str) -> bool:
        for _ in range(3):
            is_success = await self._delete_message(chat_id, message_id)

            if is_success:
                return True

            await asyncio.sleep(1)
        return False

    async def send_tips_message(self, chat_id: str, text: str, delay: int=5):
        try:
            message = await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='markdown')
            await self.set_delay_delete_msg(chat_id, str(message.message_id), delay)
        except Exception as _e:
            logger.error(_e)

    async def send_delete_tips(self, chat_id: str, user_id: str, text: str) -> Message | None:
        is_success = await self.common_service.set_delete_cache(chat_id, user_id)

        if not is_success:
            return

        await self.send_tips_message(chat_id, text, 30)


    async def set_delay_delete_msg(self, chat_id: str, message_id: str, second: int = 5):
        async def wrapper():
            await asyncio.sleep(second)
            await self.delete_message(chat_id, message_id)

        await self.common_service.add_task(wrapper())


    async def _delete_message(self, chat_id: str, message_id: str) -> bool:
        try:
            await self.bot.delete_message(chat_id, message_id)
            return True
        except MessageToDeleteNotFound:
            return True
        except Exception as _e:
            logger.error(traceback.format_exc())
            return False
