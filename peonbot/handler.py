import asyncio
import traceback
from sanic import Sanic
from sanic.log import logger
from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes

from peonbot.extensions.helper import MessageHelper

from peonbot.common import redis, command
from peonbot.bussiness.repositories import (
    ChatConfigRepository,
    BotContextRepository,
    RecordRepository
)

from peonbot.bussiness.services import (
    ChatConfigService,
    PeonService,
    RecordService,
)

from peonbot.bussiness.pipelines import GroupPipeline
from peonbot.textlang import DELETE_PATTERN


def register(app: Sanic, dp: Dispatcher):

    command_map = command.get_map(app)
    redis_factory = redis.get_factory(app)

    # Create reposities
    bot_repo = BotContextRepository(redis_factory)
    config_repo = ChatConfigRepository(redis_factory)
    record_repo = RecordRepository(redis_factory)

    # Create services
    peon_service = PeonService(dp.bot, bot_repo, app)
    chat_service = ChatConfigService(
        dp.bot,
        config_repo=config_repo,
        peon_service=peon_service
    )
    record_service = RecordService(record_repo)


    # Create pipeline
    group_pipeline = GroupPipeline(
        chat_service,
        peon_service,
        record_service,
        command_map
    )

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
            if helper.is_supergroup():
                await process_group_message(helper)

        except Exception as _e:
            print(_e)
            print(traceback.format_exc())

    async def process_group_message(helper: MessageHelper):

        # send into pipeline to check.
        ctx = await group_pipeline.invoke(helper)

        _task = []
        if ctx.mark_delete:
            _task.append(peon_service.delete_message(helper.chat_id, helper.message_id))

        if ctx.mark_record:
            _task.append(record_service.set_cache_point(helper.chat_id, helper.sender_id, ctx.point + 1))

        if ctx.msg.strip():
            fullname = helper.msg.from_user.full_name
            _text = DELETE_PATTERN.format(fullname=fullname, user_id=helper.sender_id, reason=ctx.msg)
            _task.append(peon_service.send_delete_message(helper.chat_id, helper.sender_id, _text))

        logger.debug(ctx)

        # commit to eventloop
        if len(_task) > 0:
            batch = asyncio.gather(*_task)
            app.add_task(batch)
