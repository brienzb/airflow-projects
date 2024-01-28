import datetime
import os

from dotenv import load_dotenv
from github import Auth, Github

from src.config import *


def get_github_connection() -> Github:
    global GITHUB_CONNECTION

    if GITHUB_CONNECTION is None:
        load_dotenv(dotenv_path=os.path.join(BASE_PATH, ".env"))

        auth = Auth.Token(f"{os.getenv('GITHUB_ACCESS_TOKEN')}")
        GITHUB_CONNECTION = Github(auth=auth)

    return GITHUB_CONNECTION

def get_google_trend_report_body(geography: str, google_trend_keywords: list) -> str:
    body = None
    with open(os.path.join(TEMPLATE_PATH, "report.md.template"), "r") as report_file:
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
