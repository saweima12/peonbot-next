from sanic import Sanic

from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes

from peonbot.extensions.helper import MessageHelper

from peonbot.common import redis
from peonbot.repositories import (
    ChatConfigRepository
)

from peonbot.services import (
    ChatConfigService
)

from peonbot.pipelines import MessagePipeline



def register(app: Sanic, dp: Dispatcher):

    redis_factory = redis.get_factory(app)

    # Create reposities
    config_repo = ChatConfigRepository(redis_factory)

    # Create services
    chat_service = ChatConfigService(config_repo)

    # Create pipeline
    pipeline = MessagePipeline(app)

    @dp.message_handler(content_types=ContentTypes.ANY)
    async def on_message(message: Message):
        helper = MessageHelper(message)
        
        try:
            # TODO: Check message chat avaliable.
            chat_avaliable = await chat_service.check_avaliable(helper.chat_id)
            sender_avaliable = None

            if (not chat_avaliable) and (not sender_avaliable):
                return

            # # Check message sender and content.
            # result = await pipeline.invoke(helper)

        except Exception as _e:
            print(_e)
