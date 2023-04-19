from datetime import timedelta
from sanic import Sanic

from peonbot.utils.log_util import create_logger
from peonbot.common.scheduler import TaskScheduler, AbstractTask


class TestTask(AbstractTask):
    async def run(self):
        print("run_task")


app = Sanic("test")


def test_scheduler():

    _logger = create_logger("test")
    _scheduler = TaskScheduler(app, _logger)

    # create task
    _task = TestTask()
    _scheduler.register_task(_task, "test", "*/1 * * * *", timedelta(seconds=30))

    assert _scheduler.app == app
    assert len(_scheduler.task_list()) == 1

def test_get_executor():
    _logger = create_logger("test")
    _scheduler = TaskScheduler(app, _logger)

    # create task
    _task = TestTask()
    _scheduler.register_task(_task, "test", "*/1 * * * *", timedelta(seconds=30))

    _executor = _scheduler.get_executor("test")

    now = _executor.get_now()
    delta = _executor.get_next_startdelta(now)

    assert _executor.task == _task
    assert delta == 30
