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
from bs4 import BeautifulSoup
from bs4.element import Tag
from dotenv import load_dotenv
from github import Auth, Github


GITHUB_CONNECTION = None

GOOGLE_TREND_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo={GEOGRAPHY}"
GEOGRAPHY_LIST = ["KR", "US"]

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


# Common function
def print_log(content: str, print_job_name: bool = False):
    log = f"[{datetime.datetime.now().strftime(TIMESTAMP_FORMAT)}]"
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

def get_google_trend_keywords(geography: str) -> dict:
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

def create_github_issue(content: dict):
    conn = get_github_connection()

    repo = conn.get_repo("brienzb/test")
    repo.create_issue(
        title=f"Test issue ({datetime.datetime.now()})",
        body=str(content)
    )


# Job function
def google_trend_reporting_job():
    print_log("Run google_trend_reporting_job")

    print_log("Get google trend keywords", True)
    google_trend_keywords = get_google_trend_keywords("KR")
    # pprint.pprint(google_trend_keywords)
    print_log(f"google_trend_keywords: {google_trend_keywords}", True)

    print_log("Create github issue", True)
    create_github_issue(google_trend_keywords)

    print_log("End google_trend_reporting_job")


# Main function
def main():
    sched = BackgroundScheduler()
    sched.add_job(google_trend_reporting_job, "cron", second="10", id="google_trend_reporting_job")
    sched.start()


if __name__ == "__main__":
    main()

    while True:
        print_log("Process running..")
        time.sleep(10)
