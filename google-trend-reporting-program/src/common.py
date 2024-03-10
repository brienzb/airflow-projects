import datetime
import os
import sys

from apscheduler.triggers.cron import CronTrigger

from src.config import *


def print_log(content: str, print_job_name: bool = False, only_test: bool = False):
    if only_test and os.getenv("PHASE") != "test":
        return

    log = f"[{datetime.datetime.now().strftime(LOG_TIMESTAMP_FORMAT)}]"
    if print_job_name:
        log += f" [{sys._getframe(1).f_code.co_name}]"
    print(log + f" {content}")

def get_next_run_date(geography: str) -> str:
    hour_idx = CronTrigger.FIELD_NAMES.index("hour")
    hour = int(str(GEOGRAPHY_DICT[geography]["trigger"].fields[hour_idx]))

    next_run_date = datetime.datetime.now()
    if next_run_date.hour >= hour:
        next_run_date += datetime.timedelta(days=1)

    if geography in ("KR"):
        next_run_date = next_run_date.strftime(REPORT_DATE_FORMAT)
    else:
        next_run_date = (next_run_date - datetime.timedelta(days=1)).strftime(REPORT_DATE_FORMAT)
    
    return next_run_date
