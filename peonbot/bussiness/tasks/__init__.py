from datetime import timedelta
from peonbot.common.scheduler import TaskScheduler
from peonbot.common import bot, redis

from .cache_group_admin import CacheGroupAdminTask
from .cache_to_db import CacheToDBTask

def register(scheduler: TaskScheduler, service_map: dict):

    _redis = redis.get_factory(scheduler.app)

    cache_group_admin  = CacheGroupAdminTask(**service_map)
    scheduler.register_task(cache_group_admin,
                            task_id="cache_group_admin",
                            cron_expression="*/10 * * * *")
    
    cache_to_db = CacheToDBTask(**service_map)
    scheduler.register_task(cache_to_db,
                            task_id="cache_to_db",
                            start_time=timedelta(seconds=10),
                            cron_expression="*/15 * * * *")