from typing import Tuple
from aiogram import Bot, Dispatcher
from sanic import Sanic

SERVICE_CODE = "bot"
DP_CODE = f"{SERVICE_CODE}_dp"


def get_bot(app: Sanic) -> Bot:
    return getattr(app.ctx, SERVICE_CODE)

def get_dp(app: Sanic) -> Dispatcher:
    return getattr(app.ctx, DP_CODE)

def setup(app: Sanic) -> Tuple[Bot, Dispatcher]:
    token = app.config.get("BOT_TOKEN")
    # register webhook_url.
    domain_url = app.config.get("DOMAIN_URL")
    url_prefix = app.config.get("BOT_ENDPOINT")
    webhook_url = f"{domain_url}{url_prefix}/{token}"

    bot = Bot(token)
    bot_dp = Dispatcher(bot)

    @app.main_process_start
    async def startup(_: Sanic):
        info = await bot.get_webhook_info()
        if info.url != webhook_url:
            await bot.set_webhook(webhook_url)

    @app.main_process_stop
    async def dispose(_: Sanic):
        await bot.delete_webhook()

    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, DP_CODE, bot_dp)
    return bot, bot_dp
