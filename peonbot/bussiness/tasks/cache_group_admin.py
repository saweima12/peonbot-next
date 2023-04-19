import traceback
from sanic.log import logger

from peonbot.common.scheduler import AbstractTask
from peonbot.bussiness.services import ChatConfigService, CommonService

class CacheGroupAdminTask(AbstractTask):

    def __init__(self, common_service: CommonService, chat_service: ChatConfigService, **_):
        # initialize repository & service
        self.common_service = common_service
        self.chat_service = chat_service

    async def run(self):

        chat_ids = await self.chat_service.get_avaliable_chat_ids()

        for chat_id in chat_ids:
            try:
                admin_list = await self.chat_service.get_chat_adminstrator(chat_id)
                admin_ids = [str(admin.user.id) for admin in admin_list]

                config = await self.chat_service.get_config(chat_id)
                config.adminstrators = admin_ids

                self.common_service.add_task(
                    self.chat_service.set_cache_config(chat_id, config)
                )
            except Exception:
                logger.error(traceback.format_exc())
