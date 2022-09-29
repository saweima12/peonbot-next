from datetime import datetime
from croniter import croniter as cron

print(cron("1 2 * * *").get_current(datetime))