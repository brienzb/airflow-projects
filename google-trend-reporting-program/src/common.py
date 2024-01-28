import datetime
import sys

from src.config import *


def print_log(content: str, print_job_name: bool = False, only_test: bool = False):
    if only_test and PHASE_ARGV != "test":
        return

    log = f"[{datetime.datetime.now().strftime(LOG_TIMESTAMP_FORMAT)}]"
    if print_job_name:
        log += f" [{sys._getframe(1).f_code.co_name}]"
    print(log + f" {content}")
