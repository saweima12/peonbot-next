import asyncio
from datetime import datetime
from sanic.log import logger

from peonbot.models.common import MemberLevel, PermissionLevel
from peonbot.common.scheduler import AbstractTask

from peonbot.bussiness.services import (
    CommonService,
    ChatConfigService,
    RecordService,
    PeonService
)

from peonbot.models.db import (
    PeonChatConfig
)


class CacheToDBTask(AbstractTask):

    def __init__(self,
                common_service: CommonService,
                chat_service: ChatConfigService,
                record_service: RecordService,
                peon_service: PeonService,
                **_):
        self.common_service = common_service
        self.peon_service = peon_service
        self.bot_repo = common_service.bot_repo
        self.chat_repo = chat_service.config_repo
        self.record_repo = record_service.record_repo

    async def run(self):
        # save user whitelist
        whitelist = await self.bot_repo.get_whitelist()
        await self.bot_repo.set_whitelist_db(whitelist)

        # save chat config to database.
        chats = await PeonChatConfig.filter(status="ok")

        for chat in chats:
            # save chat config
            config_cache = await self.chat_repo.get_config(chat.chat_id)
            await self.chat_repo.set_config_db(chat.chat_id, config_cache)

            # save user record
            user_records = await self.record_repo.get_record_cache(chat.chat_id)

            for user in user_records.values():
                tasks = []
                if user.member_level == MemberLevel.NONE:
                    created_time = user.created_time.replace(tzinfo=None)
                    # compare condition
                    check_speak = user.msg_count >= config_cache.senior_count
                    check_day = (datetime.utcnow() - created_time).days > config_cache.junior_day

                    if check_speak and check_day:
                        user.member_level = MemberLevel.JUNIOR
                        logger.info(f"Update {user.full_name}'s Permission to JUNIOR")
                        tasks.append(
                            self.peon_service.set_member_permission(chat.chat_id, user.user_id, PermissionLevel.ALLOW)
                        )
                # register to background.
                self.common_service.add_task(asyncio.gather(
                    self.record_repo.set_db(chat.chat_id, user),
                    *tasks
                ))

            await self.record_repo.clean_cache(chat.chat_id)
            