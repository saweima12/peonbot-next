from peonbot.repositories import ChatConfigRepository
from peonbot.models.common import Status

class ChatConfigService:

    def __init__(self, config_repo: ChatConfigRepository):
        self.config_repo = config_repo

    async def check_avaliable(self, chat_id: str) -> bool:
        config = await self.config_repo.get_config(chat_id)
        if config:
            return config.status == Status.OK
        return False

    async def check_is_admin(self, chat_id: str, user_id: str) -> bool:
        config = await self.config_repo.get_config(chat_id)
        if config:
            return user_id in set(config.adminstrators)
