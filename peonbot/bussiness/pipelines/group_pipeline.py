from datetime import datetime
from peonbot import textlang
from peonbot.common.command import CommandMap
from peonbot.extensions.helper import MessageHelper
from peonbot.models.context import MessageContext
from peonbot.models.common import Status, MemberLevel
from peonbot.models.redis import ChatConfig, UserRecord


from peonbot.bussiness.services import (
    ChatConfigService,
    PeonService,
    RecordService
)


class GroupPipeline:

    def __init__(self,
                chat_service: ChatConfigService,
                peon_service: PeonService,
                record_service: RecordService,
                command_map: CommandMap):
        self.peon_service = peon_service
        self.chat_service = chat_service
        self.record_service = record_service
        self.command_map = command_map

        self.sequence = [
            self.check_command,
            self.check_permission,
            self.check_message_type,
            self.check_message_content,
            self.check_has_url,
            self.check_need_record
        ]


    async def invoke(self, msg: MessageHelper) -> MessageContext:

        chat_config = await self.chat_service.get_config(msg.chat_id)

        # if the group isn't a registered group, direct return.
        if not chat_config.status == Status.OK:
            return None

        context = await self.cache_context(msg, chat_config)

        for handle in self.sequence:
            _next = await handle(msg, context)
            if not _next:
                break

        return context

    async def cache_context(self, msg: MessageHelper, chat_config: ChatConfig) -> MessageContext:
        # cache context.
        is_admin = msg.sender_id in set(chat_config.adminstrators)
        is_whitelist = await self.peon_service.is_whitelist(msg.sender_id)
        user_record = await self.record_service.get_record(msg.chat_id, msg.sender_id)
        member_level = self._get_member_level(user_record, chat_config)
        context = MessageContext(
            chat_config=chat_config,
            is_admin=is_admin,
            is_whitelist=is_whitelist,
            level=member_level,
            user_record=user_record,
            mark_delete=False,
            mark_record=True
        )
        return context

    async def check_command(self, helper: MessageHelper, ctx: MessageContext) -> bool:
        if helper.is_text():
            if self.command_map.is_avaliable(helper.content):
                await self.command_map.notify(helper.content, helper=helper, context=ctx)
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

        if not self._check_content_allow(helper):
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

    async def check_need_record(self, helper: MessageHelper, ctx: MessageContext):

        if not helper.is_text():
            ctx.mark_record = False
            return True

        if not len(helper.content) < 5:
            ctx.mark_record = False

        return True

    def _check_content_allow(self, helper: MessageHelper,) -> bool:

        if helper.msg.via_bot:
            return False

        if helper.get_custom_emoji():
            return False

        if helper.get_mentions():
            return False

        return True

    def _get_member_level(self, user_record: UserRecord, chat_config: ChatConfig):

        if user_record.msg_count > chat_config.senior_count:
            created_time = user_record.created_time.replace(tzinfo=None)
            offset = datetime.utcnow() - created_time
            if offset.days >= chat_config.senior_day:
                return MemberLevel.SENIOR
            elif offset.days >= chat_config.junior_day:
                return MemberLevel.JUNIOR
        return MemberLevel.NONE