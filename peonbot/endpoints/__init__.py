from sanic import Sanic, Blueprint
from . import admin, bot

def register(app: Sanic):

    # Get urlprefix from configure.
    url_prefix = app.config.get("URL_PREFIX")

    # register subpath to group & set url_prefix
    group = Blueprint.group(
        [
            admin.bp
        ],
        url_prefix=url_prefix)

    # register group to app
    app.blueprint(group)
    app.blueprint(bot.bp)
