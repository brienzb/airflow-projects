from src.common import print_log
from src.config import *
from src.github import create_github_issue, get_google_trend_report_body
from src.google_trend import get_google_trend_keywords


def google_trend_reporting_job_ver1():  # Fadeout
    print_log("Run google_trend_reporting_job")

    report_bodys = ""
    for geography in GEOGRAPHY_LIST:
        print_log(f"Get {geography} google trend keywords", print_job_name=True)
        google_trend_keywords = get_google_trend_keywords(geography)
        print_log(f"google_trend_keywords: {google_trend_keywords}", print_job_name=True, only_test=True)

        print_log(f"Get {geography} google trend report body", print_job_name=True)
        report_body = get_google_trend_report_body(geography, google_trend_keywords)
        print_log(f"report_body: {report_body}", print_job_name=True, only_test=True)

        report_bodys += report_body

    print_log("Create github issue", print_job_name=True)
    issue = create_github_issue(report_bodys)
    print_log(f"issue: {issue}", print_job_name=True, only_test=True)

    print_log("End google_trend_reporting_job")

def google_trend_reporting_job_ver2(geography: str):
    print_log("Run google_trend_reporting_job")

    report_bodys = ""
    for geography in GEOGRAPHY_LIST:
        print_log(f"Get {geography} google trend keywords", print_job_name=True)
        google_trend_keywords = get_google_trend_keywords(geography)
        print_log(f"google_trend_keywords: {google_trend_keywords}", print_job_name=True, only_test=True)

        print_log(f"Get {geography} google trend report body", print_job_name=True)
        report_body = get_google_trend_report_body(geography, google_trend_keywords)
        print_log(f"report_body: {report_body}", print_job_name=True, only_test=True)

        report_bodys += report_body

    # print_log("Create github issue", print_job_name=True)
    # issue = create_github_issue(report_bodys)
    # print_log(f"issue: {issue}", print_job_name=True, only_test=True)

    print_log("End google_trend_reporting_job")
