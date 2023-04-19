import os
from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise


from peonbot import default_config, handler, endpoints
from peonbot.common import bot, scheduler, redis, command
from peonbot.bussiness import repositories, services



def create_app() -> Sanic:
    """
    Create sanic application.
    """

    # Declare sanic instance and load default config.
    app = Sanic(__name__, env_prefix="BOT_")
    app.update_config(default_config)

    # Try loading external config with environment path.
    env_path = os.environ.get("BOT_CONFIG")
    if env_path:
        app.update_config(env_path)

    # setup redis
    redis.setup(app)

    # setup database
    db_uri = app.config.get("DB_URI")
    orm_modules = dict(
        peon_entities=["peonbot.models.db"]
    )

    register_tortoise(app,
        db_url=db_uri,
        modules=orm_modules,
        generate_schemas=True
    )


    # setup command map & scheduler
    command.setup(app)
    scheduler.setup(app)

    # setup bot & message handler
    _, _dp = bot.setup(app)
    handler.register(app, _dp)

    # register route.
    endpoints.register(app)

    return app
