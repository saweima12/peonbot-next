from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from peonbot.common.command import AbstractCommand
from peonbot.extensions.helper import MessageHelper
from peonbot.models.context import MessageContext

class TestCmd(AbstractCommand):

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("按鈕 1", callback_data="button1"))

        await helper.bot.send_message(helper.chat_id, "Weed", reply_markup=markup)
        