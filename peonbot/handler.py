from sanic import Sanic
from sanic.log import logger
from aiogram.types import Message, ContentTypes, InlineQuery, InlineQueryResultCachedSticker, InlineQueryResultCachedMpeg4Gif

from peonbot import textlang

from .services import bot
from .extension.helper import MessageHelper


def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()

    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        
        helper = MessageHelper(message)
        try:
            # process command
            if helper.is_text():
                pass
        except Exception as _e:
            pass