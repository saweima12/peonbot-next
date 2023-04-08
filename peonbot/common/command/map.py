from sanic import Sanic

SERVICE_CODE = "command_map"

def get_map():
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)
