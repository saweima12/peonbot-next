from sanic import Sanic

def get_bot_token(app: Sanic):
    return app.config.get("BOT_TOKEN")
