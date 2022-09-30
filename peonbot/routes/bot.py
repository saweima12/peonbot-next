from sanic import Blueprint, Request, response
from sanic.log import logger
from aiogram.types import Update
from peonbot.services import bot

bp = Blueprint("peon")

@bp.post("/<token:str>")
async def on_update(request: Request, token: str):
    # get bot & dp
    _bot = bot.get_bot()
    _dp = bot.get_dp()

    if token != _bot._token:
        return response.empty(200)

    update = Update(**request.json)
    logger.debug(f"on_update {update.as_json()}")
    # set default bot
    _bot.set_current(_bot)

    # dispatcher event
    await _dp.process_update(update)
    return response.empty(200)

@bp.get("/test")
async def test_me(request: Request):
    _bot = bot.get_bot()

    info = await _bot.get_me()
    return response.json(info.to_python())