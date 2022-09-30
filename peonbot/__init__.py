import os
from sanic import Sanic

from .services import bot, scheduler
from . import config, routes, handler


# define sanic application.
app = Sanic(__name__, env_prefix="BOT_")
# load default config
app.update_config(config)

# load config on environment path.
env_path = os.environ.get("BOT_CONFIG")
if env_path:
    app.update_config(env_path)

# setup services
bot.setup(app)
scheduler.setup(app)

# setup bussiness logic.
handler.register_handler(app)

# register route.
routes.register(app)
