from peonbot.textlang import TIPS_SAVE
from peonbot.common.command import AbstractCommand
from peonbot.models.context import MessageContext
from peonbot.models.db import PeonSavedMessage
from peonbot.extensions.helper import MessageHelper


class SaveCmd(AbstractCommand):

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):

        if not ctx.is_admin and not ctx.is_whitelist:
            return

        reply_msg = helper.msg.reply_to_message

        await PeonSavedMessage.update_or_create(defaults=dict(
            message_json=reply_msg.to_python()
        ), message_id=reply_msg.message_id, chat_id=reply_msg.chat.id)

        await helper.msg.reply(TIPS_SAVE)
