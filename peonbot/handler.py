from sanic import Sanic
from sanic.log import logger
from aiogram.types import Message, ContentTypes
from peonbot import textlang

from .services import bot
from .extension.msg_helper import MessageHelper

from .bussiness.group_cmd import group_cmd_map


def register_handler(app: Sanic):
    # get bot 
    dp = bot.get_dp()  
    dp.register_message_handler(on_message, content_types=ContentTypes.ANY)

async def on_message(message: Message):
    helper = MessageHelper(message)
    try:
        if helper.is_from_super_group():
            await on_group_msg(helper)
    except Exception as _e:
        logger.error(_e)
        logger.error("Process Error %s", message.as_json())

async def on_group_msg(helper: MessageHelper):
    # handle command 
    if helper.is_text():
        if group_cmd_map.is_avaliable(helper.msg.text):
            await group_cmd_map.notify(helper.msg.text, helper=helper)
            return

    helper.msg.date.hour 


async def on_private_msg(helper: MessageHelper):
    pass

