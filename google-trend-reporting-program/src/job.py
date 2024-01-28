from src.common import *
from src.config import *
from src.github import get_github_issue, create_github_issue_comment
from src.github import get_google_trend_report_body
from src.google_trend import get_google_trend_keywords


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
