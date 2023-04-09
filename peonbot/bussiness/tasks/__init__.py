from peonbot.common.scheduler import TaskScheduler
from peonbot.common import bot, redis

from .cache_group_admin import CacheGroupAdminTask

def register(scheduler: TaskScheduler):

    _bot = bot.get_bot(scheduler.app)
    _redis = redis.get_conn(scheduler.app)

    cache_group_admin  = CacheGroupAdminTask(_bot, _redis)
    scheduler.register_task(cache_group_admin,
                            task_id="cache_group_admin",
                            cron_expression="*/5 * * * *")
