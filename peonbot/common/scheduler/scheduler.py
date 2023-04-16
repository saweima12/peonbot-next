from sanic import Sanic
from sanic.log import logger
from .type import TaskScheduler

SERVICE_CODE="scheduler"

def get_scheduler(app: Sanic):
    return getattr(app.ctx, SERVICE_CODE)


def setup(app: Sanic) -> TaskScheduler:

    instance = TaskScheduler(app, logger)

    @app.after_server_start
    def startup(_):
        instance.start()

    @app.before_server_stop
    def dispose(_):
        instance.stop()

    setattr(app.ctx, SERVICE_CODE, instance)
    return instance
