import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from src.common import *
from src.config import *
from src.github import get_github_issue, create_github_issue_comment
from src.github import get_google_trend_report_body
from src.google_trend import get_google_trend_keywords


load_dotenv(dotenv_path=os.path.join(BASE_PATH, ".env"))


# Setting function
def print_phase():
    print_log(f"Phase: {os.getenv('PHASE')}")

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


# Job function
def google_trend_reporting_job(geography: str):
    global GEOGRAPHY_DICT

    print_log(f"Run {geography}_google_trend_reporting_job", print_job_name=True)

    google_trend_keywords = get_google_trend_keywords(geography)
    print_log(f"Get {geography} google trend keywords", print_job_name=True)
    print_log(f"google_trend_keywords: {google_trend_keywords}", print_job_name=True, only_test=True)

    report_body = get_google_trend_report_body(geography, google_trend_keywords)
    print_log(f"Get {geography} google trend report body", print_job_name=True)
    print_log(f"report_body: {report_body}", print_job_name=True, only_test=True)

    issue = get_github_issue(GEOGRAPHY_DICT[geography]["next_run_date"])
    print_log(f"Get github issue: {issue.title} #{issue.number}", print_job_name=True)

    issue_comment = create_github_issue_comment(issue, report_body)
    print_log(f"Create github issue comment: {issue_comment}", print_job_name=True)

    next_run_date = get_next_run_date(geography)
    GEOGRAPHY_DICT[geography]["next_run_date"] = next_run_date
    print_log(f"Set {geography} next run date: {next_run_date}", print_job_name=True)

    print_log(f"End {geography}_google_trend_reporting_job", print_job_name=True)

def schedule_jobs() -> BackgroundScheduler:
    sched = BackgroundScheduler()

    for geography, value in GEOGRAPHY_DICT.items():
        job_id = f"{geography}_google_trend_reporting_job"
        trigger = value["trigger"] if os.getenv("PHASE") == "real" else CronTrigger(second=f"{random.randint(0, 59)}")
        
        sched.add_job(google_trend_reporting_job, trigger, args=[geography], id=job_id)
        print_log(f"Set {job_id} (trigger: {trigger})")
    
    return sched


# Main function
def main():
    print_phase()
    set_geography_dict()
    set_pre_issues()

    sched = schedule_jobs()
    sched.start()


if __name__ == "__main__":
    main()

    while True:
        print_log("Process running..")
        time.sleep(PHASE[os.getenv("PHASE")]["sleep_time"])
