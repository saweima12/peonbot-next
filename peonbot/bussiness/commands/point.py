from peonbot.common.command import AbstractCommand
from peonbot.models.context import MessageContext
from peonbot.extensions.helper import MessageHelper
from peonbot.bussiness.services import RecordService, PeonService

class PointCmd(AbstractCommand):

    def __init__(self, record_service: RecordService, peon_service: PeonService, **_):
        self.record_service = record_service
        self.peon_service = peon_service

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):
        record = await self.record_service.get_record(helper.chat_id, helper.sender_id)
        msg = await helper.msg.reply(f"Point: {record.msg_count}")
        await self.peon_service.set_delay_delete_msg(helper.chat_id, msg.message_id, 5)
