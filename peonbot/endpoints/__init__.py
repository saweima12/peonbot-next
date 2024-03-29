from sanic import Sanic, Blueprint
from . import dataview, bot

def register(app: Sanic):

    # Get urlprefix from configure.
    url_prefix = app.config.get("URL_PREFIX")

    # register subpath to group & set url_prefix
    group = Blueprint.group(
        [
            dataview.register(app),
            bot.register(app)
        ],
        url_prefix=url_prefix)

    # register group to app
    app.blueprint(group)