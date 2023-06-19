from datetime import timedelta
from peonbot.common.command import AbstractCommand
from peonbot.models.context import MessageContext
from peonbot.extensions.helper import MessageHelper
from peonbot.bussiness.services import PeonService
from peonbot.models.common import PermissionLevel
from peonbot.utils.text_util import parse_int
from peonbot.textlang import TIPS_MUTE, TIPS_UNMUTE

class MuteCmd(AbstractCommand):

    def __init__(self, peon_service: PeonService, **_):
        self.peon_service = peon_service

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):


        if not ctx.is_admin and not ctx.is_whitelist:
            return

        # check parameters.
        params_count = len(args)
        if params_count != 1:
            return

        reply_msg = helper.msg.reply_to_message
        if reply_msg is None:
            return

        # get parameter.
        reply_user_id = str(reply_msg.from_user.id)
        reply_user_fullname = str(reply_msg.from_user.full_name)
        hours = parse_int(args[0])

        # set member permission
        if hours >= 1:
            await self.peon_service.set_member_permission(helper.chat_id, reply_user_id, PermissionLevel.DENY, timedelta(hours=hours))
            await reply_msg.reply(TIPS_MUTE.format(fullname=reply_user_fullname, user_id=reply_user_id, hours=hours))
        else:
            await self.peon_service.set_member_permission(helper.chat_id, reply_user_id, PermissionLevel.LIMIT, timedelta(hours=hours))
            await reply_msg.reply(TIPS_UNMUTE.format(fullname=reply_user_fullname, user_id=reply_user_id))
        