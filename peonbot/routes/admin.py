from sanic import Blueprint, Request, response
from aiogram.types import Update
from peonbot.services import bot

bp = Blueprint("dataview", url_prefix="/admin")

@bp.get("/")
async def on_login(request: Request, token: str):
    pass

