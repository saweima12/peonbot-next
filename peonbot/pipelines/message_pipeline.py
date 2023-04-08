from sanic import Sanic
from peonbot.extensions.helper import MessageHelper


class MessagePipeline:

    def __init__(self, app: Sanic):
        self.app = app

    async def invoke(self, msg: MessageHelper):
        ctx = {}
        print(msg)

    async def check_sender(self):
        pass

    async def check_type(self):
        pass

    async def check_message(self):
        pass
