import datetime
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.common import print_log
from src.config import *
from src.job import google_trend_reporting_job_ver1


def set_phase():
    global PHASE_ARGV
    
    if len(sys.argv) > 1:
        PHASE_ARGV = sys.argv[1]
    
    if PHASE_ARGV not in PHASE:
        print("Usage: python google-trend-reporting.py [test|real]")
        exit(1)
    
    print_log(f"Set phase: {PHASE_ARGV}")

def set_next_run_date():
    global GEOGRAPHY_DICT

    default_next_run_date = datetime.datetime.now()
    if default_next_run_date.hour >= 22:
        default_next_run_date += datetime.timedelta(days=1)

    for key, value in GEOGRAPHY_DICT.items():
        if key in ("KR", "JP"):
            value["next_run_date"] = default_next_run_date.strftime(REPORT_DATE_FORMAT)
        else:
            value["next_run_date"] = (default_next_run_date - datetime.timedelta(days=1)).strftime(REPORT_DATE_FORMAT)
        print_log(f"Set {key} next run date: {value['next_run_date']}")

def set_pre_issues():
    pass


# Main function
def main():
    set_phase()
    set_next_run_date()

    sched = BackgroundScheduler()
    trigger = PHASE[PHASE_ARGV]["trigger"]
    sched.add_job(google_trend_reporting_job_ver1, trigger, id="google_trend_reporting_job_ver1")

    sched.start()


if __name__ == "__main__":
    main()

    while True:
        print_log("Process running..")
        time.sleep(PHASE[PHASE_ARGV]["sleep_time"])
