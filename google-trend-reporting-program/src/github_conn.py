import os

from github import Auth, Github, Issue, IssueComment, Repository

from src.common import *
from src.config import *


GITHUB_CONNECTION = None


def get_github_connection() -> Github:
    global GITHUB_CONNECTION

    if GITHUB_CONNECTION is None:

        auth = Auth.Token(f"{os.getenv('GITHUB_ACCESS_TOKEN')}")
        GITHUB_CONNECTION = Github(auth=auth)

    return GITHUB_CONNECTION

def get_github_repo() -> Repository:
    conn = get_github_connection()
    return conn.get_repo(PHASE[os.getenv("PHASE")]["repo_name"])

def get_github_labels() -> list:
    repo = get_github_repo()
    return [repo.get_label("GTRP")]

def get_github_issue(target_date: str) -> Issue:
    repo = get_github_repo()
    labels = get_github_labels()

    issues = repo.get_issues(state="open", labels=labels)

    target_issue = None
    for issue in sorted(issues, key=lambda x: x.title):
        # Parse "[GTRP] Google Trend Report ({cmp_date})"
        cmp_date = issue.title.split(" ")[4][1:-1]

        if target_date == cmp_date:
            target_issue = issue
            break
    
    if target_issue is None:
        target_issue = create_github_issue(target_date)
    
    return target_issue

def create_github_issue(target_date: str) -> Issue:
    repo = get_github_repo()
    labels = get_github_labels()

    issue = repo.create_issue(
        title=GITHUB_ISSUE_TITLE.replace("{TARGET_DATE}", target_date),
        body=GITHUB_ISSUE_BODY,
        labels=labels
    )

    print_log(f"Create github issue: {issue.title} #{issue.number}")
    return issue

def create_github_issue_comment(issue: Issue, body: str) -> IssueComment:
    return issue.create_comment(body)


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

        rows += "|".join(row) + "\n"

    body = body.replace("{GEOGRAPHY}", GEOGRAPHY_DICT[geography]["name"])\
               .replace("{ROWS}", rows)
    
    return body
