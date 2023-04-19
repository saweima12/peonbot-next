from abc import ABC
from typing import Dict, List, Tuple
from sanic import Sanic
from peonbot.extensions.helper import MessageHelper
from peonbot.models.context import MessageContext
class AbstractCommand(ABC):

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):
        raise NotImplementedError

class CommandMap:

    def __init__(self, app: Sanic, prefix='$'):
        self.prefix = prefix
        self.app = app
        self.__handlers: Dict[str, AbstractCommand] = dict()

    @property
    def handlers(self):
        return self.__handlers

    def register_command(self, command: str, handler: AbstractCommand):
        self.__handlers[command] = handler

    def _command_split(self, text: str) -> Tuple[str, List[str]]:
        groups = text.strip().split()
        cmd = groups[0].lstrip(self.prefix)
        args = groups[1:]
        return cmd, args

    def is_avaliable(self, text: str):
        groups = text.strip().split()
        if not groups[0].startswith(self.prefix):
            return False
        cmd = groups[0].lstrip(self.prefix)
        return cmd in self.__handlers

    async def notify(self, text: str, helper: MessageHelper, ctx: MessageContext, **kwargs):
        cmd, cmd_args = self._command_split(text)
        handler = self.__handlers.get(cmd)
        if not handler:
            return

        await handler.run(*cmd_args, helper=helper, ctx=ctx, **kwargs)
        