from sanic import Sanic
from sanic.log import logger 
from peonbot.extension.msg_helper import MessageHelper


async def process(*params, helper: MessageHelper, **options):
    user_ids = Sanic.get_app().config.get("ALLOW_USERS_ID", [])
    logger.info("%s", user_ids)