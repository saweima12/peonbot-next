from sanic import Sanic
from .type import CommandMap

SERVICE_CODE = "command_map"

def get_map(app: Sanic):
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic) -> CommandMap:
    _map = CommandMap()
    setattr(app.ctx, SERVICE_CODE, _map)

    return _map
