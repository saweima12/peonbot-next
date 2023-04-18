from sanic import Sanic, Blueprint, Request, response
from sanic.log import logger
from aiogram.types import Update

from peonbot.common import bot
from peonbot.utils.bot_util import get_bot_token


def register(app: Sanic):
    bp = Blueprint("bot_endpoint", url_prefix="/bot")

    # get bot & dp
    _bot = bot.get_bot(app)
    _dp = bot.get_dp(app)

    @bp.post("/<token:str>")
    async def on_update(request: Request, token: str):
        # check url token is avaliable.
        if token != get_bot_token(request.app):
            return response.empty(200)

        update = Update(**request.json)
        logger.debug(f"on_update {update.as_json()}")
        # set default bot & dispatch event.
        _bot.set_current(_bot)
        await _dp.process_update(update)

        return response.empty(200)

    @bp.get("/test")
    async def test_me(request: Request):

        _bot = bot.get_bot(request.app)
        info = await _bot.get_me()

        return response.json(info.to_python())

    return bp