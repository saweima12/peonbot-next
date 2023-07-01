import re
import asyncio
import opencc
from peonbot import textlang
from peonbot.common.command import CommandMap
from peonbot.extensions.helper import MessageHelper
from peonbot.models.context import MessageContext
from peonbot.models.common import Status, MemberLevel
from peonbot.models.redis import ChatConfig
from peonbot.utils.text_util import check_block_name, check_arabi

from peonbot.bussiness.services import (
    ChatConfigService,
    CommonService,
    RecordService,
    PeonService
)


class GroupMessagePipeline:

    def __init__(self,
                command_map: CommandMap,
                common_service: CommonService,
                chat_service: ChatConfigService,
                record_service: RecordService,
                peon_service: PeonService,
                **_):
        self.common_service = common_service
        self.chat_service = chat_service
        self.record_service = record_service
        self.peon_service = peon_service
        self.command_map = command_map
        self.converter = opencc.OpenCC("s2tw")

        self.check_sequence = [
            self.check_command,
            self.check_permission,
            self.check_message_type,
            self.check_message_content,
            self.check_block_char,
            self.check_spchinese_name,
            self.check_spchinese_content,
            self.check_has_url,
            self.check_need_record,
        ]


    async def invoke(self, msg: MessageHelper) -> MessageContext:

        chat_config = await self.chat_service.get_config(msg.chat_id)

        # if the group isn't a registered group, direct return.
        if not chat_config.status == Status.OK:
            return None

        context = await self.__cache_context(msg, chat_config)

        for handle in self.check_sequence:
            _next = await handle(msg, context)
            if not _next:
                break

        return context

    async def check_command(self, helper: MessageHelper, ctx: MessageContext) -> bool:
        if helper.is_text():
            if self.command_map.is_avaliable(helper.content):
                await self.command_map.notify(helper.content, helper=helper, ctx=ctx)
                ctx.mark_record = False
                return False

        return True

    async def check_permission(self, _:MessageHelper, ctx: MessageContext) -> bool:
        if ctx.is_admin:
            return False
        return True

    async def check_message_type(self, helper: MessageHelper, ctx: MessageContext) -> bool:

        if ctx.level >= MemberLevel.JUNIOR:
            return True

        if helper.is_forward():
            ctx.mark_delete = True
            ctx.mark_record = False
            ctx.msg = textlang.REASON_EXTERNAL_FORWARD
            return False

        if not helper.is_text():
            ctx.mark_delete = True
            ctx.mark_record = False
            ctx.msg = textlang.REASON_MEDIA
            return False

        return True

    async def check_message_content(self, helper: MessageHelper, ctx: MessageContext):

        if ctx.level >= MemberLevel.JUNIOR:
            return True

        if not self.__check_content_allow(helper):
            ctx.mark_delete = True
            ctx.mark_record = False
            ctx.msg = textlang.REASON_MEDIA
            return False

        return True

    async def check_has_url(self, helper: MessageHelper, ctx: MessageContext):

        if ctx.level >= MemberLevel.JUNIOR:
            return True

        if helper.has_url():
            ctx.mark_delete = True
            ctx.mark_record = False
            ctx.msg = textlang.REASON_EXTERNAL_LINK
            return False

        return True

    async def check_spchinese_name(self, helper: MessageHelper, ctx: MessageContext):

        if ctx.level >= MemberLevel.JUNIOR:
            return True

        point = 0
        # fetch all chinese word.
        words = re.findall(r"([^u4E00-u9FA5])", helper.sender_fullname)
        origin_str = "".join(words).strip()
        tc_str = self.converter.convert(origin_str)

        for index, value in enumerate(tc_str):
            if value != origin_str[index]:
                point += 1

                if point >= 1:
                    break

        if point >= 1:
            ctx.mark_record = False
            ctx.mark_delete = True
            ctx.msg = textlang.REASON_BLOCK_NAME

        return True

    async def check_spchinese_content(self, helper:MessageHelper, ctx: MessageContext):

        if ctx.level >= MemberLevel.JUNIOR:
            return True

        point = 0
        # fetch all chinese word.
        words = re.findall(r"([^u4E00-u9FA5])", helper.content)
        origin_str = "".join(words).strip()
        tc_str = self.converter.convert(origin_str)

        for index, value in enumerate(tc_str):
            if value != origin_str[index]:
                point += 1

                if point >= 1:
                    break

        if point >= 1:
            ctx.mark_record = False
            ctx.mark_delete = True
            ctx.msg = textlang.REASON_BLOCK_SCINESE
            return False

        return True
    
    async def check_block_char(self, helper: MessageHelper, ctx:MessageContext):
        
        if ctx.level >= MemberLevel.JUNIOR:
            return True

        if check_arabi(helper.msg.text):
            ctx.mark_record = False
            ctx.mark_delete = True
            ctx.msg = textlang.REASON_BLOCK_SCINESE
            return False
        return True

    async def check_need_record(self, helper: MessageHelper, ctx: MessageContext):

        if not helper.is_text():
            ctx.mark_record = False
            return True

        if not len(helper.content) < 5:
            ctx.mark_record = False

        return True

    async def process_message(self, helper: MessageHelper, ctx: MessageContext):

        _task = []
        if ctx.mark_delete:
            _task.append(self.peon_service.process_delete(helper, ctx))
            content_type = "forward" if helper.is_forward() else helper.content_type
            _task.append(
                self.common_service.record_delete_message(helper.chat_id, content_type, helper.msg.to_python())
            )

        if ctx.mark_record:
            record = ctx.user_record
            record.msg_count += 1
            record.full_name = helper.sender_fullname
            _task.append(
                self.record_service.set_cache_record(helper.chat_id, record)
            )

        if len(_task) >= 1:
            self.common_service.add_task(asyncio.gather(*_task))


    def __check_content_allow(self, helper: MessageHelper,) -> bool:

        if helper.msg.via_bot:
            return False

        if helper.get_custom_emoji():
            return False

        if helper.get_mentions():
            return False

        return True

    async def __cache_context(self, msg: MessageHelper, chat_config: ChatConfig) -> MessageContext:
        # cache context.
        is_admin = msg.sender_id in set(chat_config.adminstrators)
        is_whitelist = await self.common_service.is_whitelist(msg.sender_id)
        user_record = await self.record_service.get_record(msg.chat_id, msg.sender_id)

        context = MessageContext(
            chat_config=chat_config,
            is_admin=is_admin,
            is_whitelist=is_whitelist,
            level=user_record.member_level,
            user_record=user_record,
            mark_delete=False,
            mark_record=True
        )
        return context
