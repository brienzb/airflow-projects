import random
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.common import *
from src.config import *
from src.github import get_github_issue
from src.job import google_trend_reporting_job


def set_phase():
    global PHASE_ARGV
    
    if len(sys.argv) > 1:
        PHASE_ARGV = sys.argv[1]
    
    if PHASE_ARGV not in PHASE:
        print("Usage: python google-trend-reporting.py [test|real]")
        exit(1)
    
    print_log(f"Set phase: {PHASE_ARGV}")

def set_geography_dict():
    global GEOGRAPHY_DICT

    for geography in GEOGRAPHY_DICT.keys():
        next_run_date = get_next_run_date(geography)

        GEOGRAPHY_DICT[geography]["next_run_date"] = next_run_date
        print_log(f"Set {geography} next run date: {next_run_date}")

def set_pre_issues():
    sorted_geography_dict = dict(sorted(GEOGRAPHY_DICT.items(), key=lambda x: x[1]["next_run_date"]))

    for _, value in sorted_geography_dict.items():
        issue = get_github_issue(value["next_run_date"])
        print_log(f"Set github issue: {issue.title} #{issue.number}")

def schedule_jobs() -> BackgroundScheduler:
    sched = BackgroundScheduler()

    for geography, value in GEOGRAPHY_DICT.items():
        job_id = f"{geography}_google_trend_reporting_job"
        trigger = value["trigger"] if PHASE_ARGV == "real" else CronTrigger(second=f"{random.randint(0, 59)}")
        
        sched.add_job(google_trend_reporting_job, trigger, args=[geography], id=job_id)
        print_log(f"Set {job_id} (trigger: {trigger})")
    
    return sched


# Main function
def main():
    set_phase()
    set_geography_dict()
    set_pre_issues()

    sched = schedule_jobs()
    sched.start()


if __name__ == "__main__":
    main()

    while True:
        print_log("Process running..")
        time.sleep(PHASE[PHASE_ARGV]["sleep_time"])
