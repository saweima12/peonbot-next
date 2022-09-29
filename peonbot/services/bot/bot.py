from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes, InlineQuery
from sanic import Sanic

SERVICE_CODE = "bot"
DP_CODE = f"{SERVICE_CODE}_dp" 


def get_bot() -> Bot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def get_dp() -> Dispatcher:
    app = Sanic.get_app()
    return getattr(app.ctx, DP_CODE)

def setup(app: Sanic):
    token = app.config.get("BOT_TOKEN")
    domain_url = app.config.get("DOMAIN_URL")
    url_prefix = app.config.get("URL_PREFIX")
    webhook_url = f"{domain_url}{url_prefix}{token}"

    bot = Bot(token)
    dp = Dispatcher(bot)
    
    @app.main_process_start
    async def startup(app: Sanic):
        info = await bot.get_webhook_info()
        if not (info.url == webhook_url):
            await bot.set_webhook(webhook_url)

    @app.before_server_stop
    async def dispose(app: Sanic):
        await bot.delete_webhook()


    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, DP_CODE, dp)
