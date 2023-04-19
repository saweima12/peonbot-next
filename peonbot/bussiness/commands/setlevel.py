import asyncio
from peonbot.textlang import TIPS_SETLEVEL
from peonbot.models.common import MemberLevel, PermissionLevel
from peonbot.models.context import MessageContext
from peonbot.extensions.helper import MessageHelper
from peonbot.common.command import AbstractCommand
from peonbot.bussiness.services import CommonService, PeonService, RecordService

class SetLevelCmd(AbstractCommand):

    def __init__(self,
                common_service: CommonService,
                peon_service: PeonService, 
                record_service: RecordService, 
                **_):
        self.common_service = common_service
        self.peon_service = peon_service
        self.record_service = record_service

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):

        if not ctx.is_admin and not ctx.is_whitelist:
            return

        # check parameters.
        params_count = len(args)
        if params_count != 1:
            return

        param_map = {
            'jr': MemberLevel.JUNIOR,
            'sr': MemberLevel.SENIOR,
            'none': MemberLevel.NONE
        }

        if args[0] not in param_map:
            return

        # check reply message exists.
        print(helper.msg)

        reply_msg = helper.msg.reply_to_message
        if reply_msg is None:
            return

        # get parameter.
        reply_user_id = str(reply_msg.from_user.id)
        reply_full_name = reply_msg.from_user.full_name
        record = await self.record_service.get_record(helper.chat_id, reply_user_id)

        # set member level
        record.member_level = param_map.get(args[0], MemberLevel.NONE)

        # execute task
        tasks = [
            self.record_service.set_cache_record(helper.chat_id, record),
            self.record_service.set_db_record(helper.chat_id, record),
        ]

        target_permission = PermissionLevel.LIMIT  if record.member_level == MemberLevel.NONE else PermissionLevel.ALLOW
        tasks.append(self.peon_service.set_member_permission(helper.chat_id, reply_user_id, target_permission))

        # Add tips message task
        text = TIPS_SETLEVEL.format(fullname=reply_full_name, user_id=reply_user_id, level=args[0])
        tasks.append(self.peon_service.send_tips_message(helper.chat_id, text, 5))

        # remove set message
        tasks.append(helper.msg.delete())

        self.common_service.add_task(asyncio.gather(*tasks))
