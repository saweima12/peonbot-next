from sanic import Sanic
from peonbot.extensions.helper import MessageHelper

from peonbot.bussiness.services import ChatConfigService

class MessagePipeline:

    def __init__(self, chat_service: ChatConfigService):
        self.chat_service = chat_service

    async def invoke(self, msg: MessageHelper):
        ctx = {}
        print(msg)

