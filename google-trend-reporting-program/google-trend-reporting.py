import datetime
import html
import os
# import pprint
import re
import requests
import sys
import time
import unicodedata

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv
from github import Auth, Github


PHASE = {
    "real": {
        "repo_name": "brienzb/test",
        "trigger": CronTrigger(hour='10,22'),
        "sleep_time": 600,
    },
    "test": {
        "repo_name": "brienzb/test",
        "trigger": CronTrigger(second='0,30'),
        "sleep_time": 10,
    }
}
PHASE_ARGV = "test"

GITHUB_CONNECTION = None

GOOGLE_TREND_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo={GEOGRAPHY}"
GEOGRAPHY_LIST = ["US", "KR"]

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
REPORT_DATE_FORMAT = "%Y-%m-%d %H"


# Common function
def set_phase():
    global PHASE_ARGV
    
    if len(sys.argv) > 1:
        PHASE_ARGV = sys.argv[1]
    
    if PHASE_ARGV not in PHASE:
        print("Usage: python google-trend-reporting.py [test|real]")
        exit(1)
    
    print_log(f"Set phase: {PHASE_ARGV}")

def print_log(content: str, print_job_name: bool = False, only_test: bool = False):
    if only_test and PHASE_ARGV != "test":
        return

    log = f"[{datetime.datetime.now().strftime(LOG_TIMESTAMP_FORMAT)}]"
    if print_job_name:
        log += f" [{sys._getframe(1).f_code.co_name}]"
    print(log + f" {content}")


# Google trend function
def parse_google_trend_keyword(item: Tag) -> dict:
    def _decoded_tag(tag: Tag) -> str:
        text = html.unescape(tag.text)
        return unicodedata.normalize("NFKD", text)

    title = _decoded_tag(item.find("title"))
    approx_traffic = _decoded_tag(item.find("ht:approx_traffic"))

    approx_traffic_num = int(re.sub("[,+]", "", approx_traffic))

    news_title_list = item.find_all("ht:news_item_title")
    news_snippet_list = item.find_all("ht:news_item_snippet")
    news_url_list = item.find_all("ht:news_item_url")
    news_source_list = item.find_all("ht:news_item_source")

    news = []
    for idx in range(len(news_title_list)):
        news.append({
            "title": _decoded_tag(news_title_list[idx]),
            "snippet": _decoded_tag(news_snippet_list[idx]),
            "url": _decoded_tag(news_url_list[idx]),
            "source": _decoded_tag(news_source_list[idx]),
        })
    
    return {
        "title": title,
        "approx_traffic": approx_traffic,
        "approx_traffic_num": approx_traffic_num,
        "news": news,
    }

def get_google_trend_keywords(geography: str) -> list:
    google_trend_url = GOOGLE_TREND_RSS_URL.replace("{GEOGRAPHY}", geography)

    response = requests.get(google_trend_url)
    if response.status_code != 200:
        print(f"[ERROR] Request failed (status code: {response.status_code})")
        return {}
    
    xml = response.content
    soup = BeautifulSoup(xml, "xml")
    
    items = soup.find_all("item")

    google_trend_keywords = []
    rank, prev_approx_traffic_num = 1, None
    for item in items:
        keyword = parse_google_trend_keyword(item)
        
        if prev_approx_traffic_num is None:
            prev_approx_traffic_num = keyword["approx_traffic_num"]
        elif prev_approx_traffic_num < keyword["approx_traffic_num"]:
            break
        else:
            prev_approx_traffic_num = keyword["approx_traffic_num"]

        keyword["rank"] = rank
        google_trend_keywords.append(keyword)

        rank += 1
    
    return google_trend_keywords


# Github function
def get_github_connection() -> Github:
    global GITHUB_CONNECTION

    if GITHUB_CONNECTION is None:
        load_dotenv()

        auth = Auth.Token(f"{os.getenv('GITHUB_ACCESS_TOKEN')}")
        GITHUB_CONNECTION = Github(auth=auth)

    return GITHUB_CONNECTION

def get_google_trend_report_body(geography: str, google_trend_keywords: list) -> str:
    body = None
    with open("./report.md.template", "r") as report_file:
        body = report_file.read()

    rows = ""
    for keyword in google_trend_keywords:
        row = [str(keyword["rank"]), keyword["title"], keyword["approx_traffic"]]
        
        news_contents = []
        for news in keyword["news"]:
            news_contents.append(f"<a href='{news['url']}'>{news['title']}</a>")
        row.append("<br>".join(news_contents))

        print(row)
        rows += "|".join(row) + "\n"

    body = body.replace("{GEOGRAPHY}", geography)\
               .replace("{ROWS}", rows)
    
    return body

def create_github_issue(body: str) -> dict:
    conn = get_github_connection()

    repo = conn.get_repo(PHASE[PHASE_ARGV]["repo_name"])
    label = repo.get_label("GTRP")

    title = f"[GTRP] Google Trend Report ({datetime.datetime.now().strftime(REPORT_DATE_FORMAT)})"

    repo.create_issue(title=title, body=body, labels=[label])
    return {
        "title": title,
        "body": body,
    }


# Job function
def google_trend_reporting_job():
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


# Main function
def main():
    set_phase()

    sched = BackgroundScheduler()
    trigger = PHASE[PHASE_ARGV]["trigger"]
    sched.add_job(google_trend_reporting_job, trigger, id="google_trend_reporting_job")

    sched.start()


if __name__ == "__main__":
    main()

    while True:
        print_log("Process running..")
        time.sleep(PHASE[PHASE_ARGV]["sleep_time"])
