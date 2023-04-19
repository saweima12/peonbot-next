import asyncio
from typing import List
from aiogram import Bot
from peonbot.bussiness.repositories import ChatConfigRepository
from peonbot.models.common import Status

from peonbot.models.redis import ChatConfig
from .common_service import CommonService

class ChatConfigService:

    def __init__(self, bot: Bot,
                 config_repo: ChatConfigRepository,
                 common_service: CommonService):
        self.bot = bot
        self.config_repo = config_repo
        self.common_service = common_service

    async def register_chat(self, chat_id: str, chat_name: str, sender_id: str) -> bool:

        config = await self.get_config(chat_id)

        # Check sender's id is in the whitelist
        sender_avaliable = await self.common_service.is_whitelist(sender_id)

        if (config.status == Status.UNKNOWN) and not sender_avaliable:
            return False

        is_admin = await self.is_admin(chat_id, sender_id)

        if not is_admin and not sender_avaliable:
            return False

        # get chat's adminstrators
        administrators = await self.get_chat_adminstrator(chat_id)
        admin_ids = [str(admin.user.id) for admin in administrators]

        config.status = Status.OK
        config.chat_name = chat_name
        config.adminstrators = admin_ids

        await asyncio.gather(
            self.config_repo.set_config_cache(chat_id, config),
            self.config_repo.set_config_db(chat_id, config)
        )

        return True

    async def get_config(self, chat_id: str) -> ChatConfig:
        result = await self.config_repo.get_config(chat_id)
        if result is not None:
            return result

        _config = ChatConfig(chat_id=chat_id)
        await self.config_repo.set_config_cache(chat_id, _config)
        return _config

    async def set_cache_config(self, chat_id: str, data: ChatConfig):
        await self.config_repo.set_config_cache(chat_id, data)

    async def check_avaliable(self, chat_id: str) -> bool:
        config = await self.config_repo.get_config(chat_id)
        if config:
            return config.status == Status.OK
        return False

    async def is_admin(self, chat_id: str, user_id: str) -> bool:
        config = await self.config_repo.get_config(chat_id)
        if config:
            return user_id in set(config.adminstrators)
        return False

    async def get_chat_adminstrator(self, chat_id: str):
        administrators = await self.bot.get_chat_administrators(chat_id)
        return administrators

    async def get_avaliable_chat_ids(self) -> List[str]:
        return await self.config_repo.get_avaliable_chat_ids()
