import asyncio
from optparse import Option
from typing import Callable, Mapping, Optional
from datetime import datetime, timedelta

from croniter import croniter
from sanic import Sanic



class CronTask:

    def __init__(self, task_id: str, 
                       callback: Callable, 
                       cron_expression: str | None, 
                       start_time: datetime | None,
                       utc: bool):
        self.task_id = task_id
        self.callback = callback
        self.cron_expression = cron_expression
        self.start_time = start_time
        self.utc = utc
        self.__run_task: asyncio.Task | None = None

    def _get_next_delta(self) -> int:
        # get current time
        now = datetime.utcnow().replace(microsecond=0)
        if not self.utc:
            now = datetime.now().replace(microsecond=0)

        if not self.cron_expression:
            pass
            
        
    def run(self):
        next_delta = self._get_next_delta()

    def start(self, app: Sanic):
        self.__run_task = app.add_task(self.callback)

    def stop(self):
        if self.__run_task:
            self.__run_task.cancel()


class CronScheudler:

    def __init__(self):
        self._task_map: Mapping[str, CronTask] = {}

    @property
    def task_map(self):
        return self._task_map

    def get_task(self, task_id: str) -> CronTask | None:
        return self._task_map.get(task_id, default=None)
    
    def register_task_handler(self, task_id: str, 
                                    func: Callable, 
                                    cron_expression: Optional[str] = None,
                                    start_time: Optional[datetime] = None,
                                    utc: Optional[bool] = True):
        self._task_map[task_id] = CronTask(task_id, func, cron_expression, start_time, utc)

    def register_task(self, task_id: str, 
                            cron_expression: Optional[str] = None, 
                            start_time: Option[datetime] = None,
                            utc: Optional[bool] = True):
        def wrapper(callback: Callable):
            self.register_task_handler(task_id, callback, cron_expression, start_time,  utc)
        return wrapper
        