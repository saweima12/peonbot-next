import traceback
from sanic import Sanic
from sanic.log import logger
from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes

from peonbot.extensions.helper import MessageHelper

from peonbot.common import redis
from peonbot.bussiness.repositories import (
    ChatConfigRepository,
    BotConfigRepository
)

from peonbot.bussiness.services import (
    ChatConfigService,
    PeonService
)

from peonbot.bussiness.pipelines import MessagePipeline


def register(app: Sanic, dp: Dispatcher):

    redis_factory = redis.get_factory(app)

    # Create reposities
    bot_repo = BotConfigRepository(redis_factory)
    config_repo = ChatConfigRepository(redis_factory)

    # Create services
    peon_service = PeonService(dp.bot, bot_repo)
    chat_service = ChatConfigService(
        dp.bot,
        config_repo=config_repo,
        peon_service=peon_service
    )

    # Create pipeline
    pipeline = MessagePipeline(app)

    @dp.message_handler(commands=['start'])
    async def on_start(message: Message):

        helper = MessageHelper(message)
        logger.info(f"On Start: {message}")

        try:
            is_success = await chat_service.register_chat(
                helper.chat_id,
                helper.chat_name,
                helper.sender_id
            )

            if not is_success:
                return

            await helper.bot.send_message(helper.chat_id, f"Register chat {helper.chat_name} success.")

        except Exception as _e:
            logger.error(_e)
            logger.error(traceback.format_exc())



    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        helper = MessageHelper(message)

        try:
            chat_avaliable = await chat_service.check_avaliable(helper.chat_id)
            sender_avaliable = await peon_service.is_whitelist(helper.sender_id)

            if (not chat_avaliable) and (not sender_avaliable):
                return

            # TODO: Check message chat avaliable.
            # # Check message sender and content.
            # result = await pipeline.invoke(helper)

        except Exception as _e:
            print(_e)
