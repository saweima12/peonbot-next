import asyncio
import traceback
from sanic import Sanic
from sanic.log import logger
from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes, ChatType, CallbackQuery

from peonbot.common import redis, command, scheduler
from peonbot.models.common import MemberLevel, PermissionLevel
from peonbot.extensions.helper import MessageHelper
from peonbot.bussiness import commands, tasks
from peonbot.bussiness.repositories import (
    ChatConfigRepository,
    BotContextRepository,
    RecordRepository
)
from peonbot.bussiness.services import (
    CommonService,
    ChatConfigService,
    RecordService,
    PeonService
)

from peonbot.bussiness.pipelines import GroupMessagePipeline


def register(app: Sanic, dp: Dispatcher):

    command_map = command.get_map(app)
    redis_factory = redis.get_factory(app)
    _scheduler = scheduler.get_scheduler(app)

    # Create reposities
    bot_repo = BotContextRepository(redis_factory)
    config_repo = ChatConfigRepository(redis_factory)
    record_repo = RecordRepository(redis_factory)

    # Create services
    common_service = CommonService(app, bot_repo)
    chat_service = ChatConfigService(
        dp.bot,
        config_repo=config_repo,
        common_service=common_service
    )
    record_service = RecordService(record_repo)
    peon_service = PeonService(dp.bot, common_service, record_service)

    service_map = dict(
        common_service=common_service,
        chat_service=chat_service,
        record_service=record_service,
        peon_service=peon_service,
    )

    # register task & command
    tasks.register(_scheduler, service_map)
    commands.register(command_map, service_map)

    # Create pipeline
    group_msg_pipeline = GroupMessagePipeline(
        command_map,
        **service_map
    )

    @dp.message_handler(chat_type=ChatType.SUPERGROUP, commands=['start'])
    async def on_start(message: Message):

        helper = MessageHelper(message)
        logger.info(f"On Start: {message}")

        try:
            is_success = await chat_service.register_chat(helper.chat_id, helper.chat_name, helper.sender_id)

            if not is_success:
                return

            await helper.bot.send_message(helper.chat_id, f"Register chat {helper.chat_name} success.")

        except Exception as _e:
            logger.error(_e)
            logger.error(traceback.format_exc())

    @dp.message_handler(chat_type=ChatType.SUPERGROUP, content_types=ContentTypes.NEW_CHAT_MEMBERS)
    async def on_enter_group(message: Message):
        helper = MessageHelper(message)
        logger.debug(f"ChatMemberHandler: {message}")
        try:
            is_avaliable = await chat_service.check_avaliable(helper.chat_id)

            if not is_avaliable:
                return

            _tasks = [helper.msg.delete()]
            # check user level.
            user_record = await record_service.get_record(helper.chat_id, helper.sender_id)
            if user_record.member_level < MemberLevel.JUNIOR:
                _tasks.append(peon_service.set_member_permission(
                    helper.chat_id,
                    helper.sender_id,
                    PermissionLevel.LIMIT
                ))

            # Execute task
            common_service.add_task(asyncio.gather(*_tasks))


        except Exception as _e:
            logger.error(_e)
            logger.error(traceback.format_exc())

    @dp.message_handler(chat_type=ChatType.SUPERGROUP, content_types=ContentTypes.LEFT_CHAT_MEMBER)
    async def on_leave_group(message: Message):

        helper = MessageHelper(message)
        is_avaliable = await chat_service.check_avaliable(helper.chat_id)
        if not is_avaliable:
            return
        await message.delete()

    @dp.message_handler(chat_type=ChatType.SUPERGROUP, content_types=ContentTypes.ANY)
    async def on_group_message(message: Message):
        helper = MessageHelper(message)

        try:
            # send into pipeline to check.
            ctx = await group_msg_pipeline.invoke(helper)
            logger.debug(f"Context {ctx}")

            # when group is not registered, ignore it.
            if not ctx:
                return
            
            # prcoess message.
            await group_msg_pipeline.process_message(helper, ctx)

        except Exception as _e:
            logger.error(_e)
            logger.error(traceback.format_exc())


    @dp.callback_query_handler()
    async def on_callback_query(query: CallbackQuery):
        logger.info(query)
        await query.answer("投票成功")
