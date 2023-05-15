import asyncio
import traceback
from typing import Optional
from datetime import timedelta
from sanic.log import logger

from aiogram import Bot
from aiogram.types import ChatPermissions
from aiogram.utils.exceptions import MessageToDeleteNotFound

from peonbot.textlang import DELETE_PATTERN, MUTE_PATTERN
from peonbot.extensions.helper import MessageHelper
from peonbot.models.common import PermissionLevel
from peonbot.models.context import MessageContext
from peonbot.bussiness.services import CommonService, RecordService

class PeonService:

    def __init__(self, bot: Bot, common_service: CommonService, record_service: RecordService):
        self.bot = bot
        self.common_service = common_service
        self.record_service = record_service

    async def process_delete(self, helper: MessageHelper, ctx: MessageContext):
        # try to delete message.
        for _ in range(3):
            is_success = await self._send_delete_request(helper.chat_id, helper.message_id)
            if is_success:
                break
            await asyncio.sleep(1)

        count = await self.common_service.set_delete_cache(helper.chat_id, helper.sender_id)

        # count greater than 1 means that tips have been sent
        if count > 1:
            return

        # process deleted tips.
        fullname = helper.msg.from_user.full_name

        if count >= 3:
            text = MUTE_PATTERN.format(fullname=fullname, user_id=helper.sender_id)
            self.common_service.add_task(asyncio.gather(
                self.set_member_permission(helper.chat_id, helper.sender_id, PermissionLevel.DENY, timedelta(days=3)),
                self.send_tips_message(helper.chat_id, text)
            ))
            return

        text = DELETE_PATTERN.format(fullname=fullname, user_id=helper.sender_id, reason=ctx.msg)

        self.common_service.add_task(asyncio.gather(
            self.set_member_permission(helper.chat_id, helper.sender_id, PermissionLevel.LIMIT),
            self.send_tips_message(helper.chat_id, text, 30)
        ))

    async def set_member_permission(self,
                                    chat_id: str,
                                    user_id: str,
                                    level: PermissionLevel,
                                    until_date: Optional[timedelta] = None):
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

        return await self.bot.restrict_chat_member(chat_id, int(user_id), permissions=permission, until_date=until_date)

    async def send_tips_message(self, chat_id: str, text: str, delay: int=0):
        try:
            message = await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='markdown')

            if delay > 0:
                self.delay_delete_task(chat_id, str(message.message_id), delay)
        except Exception as _e:
            logger.error(_e)

    def delay_delete_task(self, chat_id: str, message_id: str, second: int = 5):
        async def wrapper():
            await asyncio.sleep(second)
            await self._send_delete_request(chat_id, message_id)

        self.common_service.add_task(wrapper())

    async def _send_delete_request(self, chat_id: str, message_id: str) -> bool:
        try:
            await self.bot.delete_message(chat_id, message_id)
            return True
        except MessageToDeleteNotFound:
            return True
        except Exception as _e:
            logger.error(traceback.format_exc())
            return False
