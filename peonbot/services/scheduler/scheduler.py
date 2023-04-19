from sanic import Sanic
from sanic.log import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

SERVICE_CODE = "scheduler"

def get() -> AsyncIOScheduler:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic) -> AsyncIOScheduler:
    _scheduler = AsyncIOScheduler()

    @app.after_server_start
    def after_start(app: Sanic):
        logger.info("Startup Scheduler service...")
        _scheduler.start()

    @app.before_server_stop
    def before_stop(app: Sanic):
        _scheduler.shutdown()

    setattr(app.ctx, SERVICE_CODE, _scheduler)