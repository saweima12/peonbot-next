import asyncio
import traceback
import logging
from abc import ABC, abstractmethod
from typing import Mapping, List
from datetime import datetime, timedelta

from sanic import Sanic
from croniter import croniter

class AbstractTask(ABC):

    @abstractmethod
    async def run(self):
        pass


class TaskExecutor():

    def __init__(self,
                task_id: str,
                task: AbstractTask,
                utc: bool,
                cron_expression: str | None = None,
                start_time: timedelta | None = None,
                logger: logging.Logger | None = None):
        self.task_id = task_id
        self.task = task
        self.cron_expression = cron_expression
        self.start_time = start_time
        self.utc = utc
        self.logger = logger
        self._first_run = True
        self._scheduler = None
        self._runtask = None

        if self.cron_expression:
            self.croniter = croniter(cron_expression)

    @staticmethod
    def create(
            task_id: str,
            task: AbstractTask,
            utc: bool,
            cron_expression: str | None = None,
            start_time: timedelta | None = None,
            logger: logging.Logger | None = None
        ) -> "TaskExecutor":
        if cron_expression and not croniter.is_valid(cron_expression):
            logger.warn(f"The cron {cron_expression} expression is not avaliable.")
            return None

        return TaskExecutor(task_id, task, utc, cron_expression, start_time, logger)


    def set_scheduler(self, scheduler: "TaskScheduler"):
        self._scheduler = scheduler

    def set_runtask(self, run_task: asyncio.Task):
        self._runtask = run_task

    async def run(self):
        while True:
            now = self.get_now()
            next_delta = self.get_next_startdelta(now)

            if next_delta:
                await asyncio.sleep(next_delta)

            try:
                self.logger.debug(f"Task start: {self.task_id}")
                self._first_run = False

                await self.task.run()

                self.logger.debug(f"Task finished: {self.task_id}")

                if next_delta <= 0:
                    break

            except Exception as _e:
                self.logger.error(traceback.format_exc())


    def get_now(self):
        if not self.utc:
            return datetime.now().replace(microsecond=0)
        return datetime.utcnow().replace(microsecond=0)

    def get_next_startdelta(self, now: datetime):

        if (self.start_time is not None) and self._first_run:
            if isinstance(self.start_time, timedelta):
                return int(self.start_time.total_seconds())

        # After first_run.
        if self.croniter is None:
            return -1

        _next_start_time: datetime = self.croniter.get_next(datetime, now)
        while _next_start_time <= now:
            _next_start_time = self.croniter.get_next(datetime, _next_start_time)

        return int((_next_start_time - now).seconds)

    def cacnel(self):
        return self._runtask.cancel()

class TaskScheduler:

    def __init__(self, app: Sanic, logger: logging.Logger):
        self.__executor_map: Mapping[str, TaskExecutor] = {}
        self.app = app
        self.logger = logger

    def register_task(self,
                    task: AbstractTask,
                    task_id: str,
                    cron_expression: str | None = None,
                    start_time: timedelta | None = None,
                    utc: bool=True):
        executor = TaskExecutor.create(task_id, task, utc, cron_expression, start_time, self.logger)
        self.__executor_map[task_id] = executor

    def get_executor(self, task_id) -> TaskExecutor:
        return self.__executor_map.get(task_id)

    def start(self):
        for executor in self.__executor_map.values():
            self.__schedule_task(executor)

    def stop(self):
        for executor in self.__executor_map.values():
            executor.cacnel()

    def task_list(self) -> List[str]:
        return self.__executor_map.keys()

    def __schedule_task(self, executor: TaskExecutor):
        run_task = self.app.add_task(executor.run)
        executor.set_runtask(run_task)
