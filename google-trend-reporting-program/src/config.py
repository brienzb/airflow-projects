import os

from apscheduler.triggers.cron import CronTrigger


BASE_PATH = os.path.dirname(os.path.dirname(__file__))  # google-trend-reporting-program repository
TEMPLATE_PATH = os.path.join(BASE_PATH, "template")

PHASE = {
    "real": {
        "repo_name": "brienzb/toy-box",
        "sleep_time": 600,  # 10 minutes
    },
    "test": {
        "repo_name": "brienzb/test",
        "sleep_time": 10,  # 10 seconds
    }
}

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
REPORT_DATE_FORMAT = "%Y-%m-%d"

GOOGLE_TREND_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo={GEOGRAPHY}"
GEOGRAPHY_DICT = {
    "KR": {
        "name": "Korea",
        "trigger": CronTrigger(hour='22'),  # 10 p.m. in KTS
    },
    "FR": {
        "name": "France",
        "trigger": CronTrigger(hour='6'),  # 10 p.m. in KTS
    },
    "CH": {
        "name": "Swiss",
        "trigger": CronTrigger(hour='6'),  # 10 p.m. in KTS
    },
    "GB": {
        "name": "UK",
        "trigger": CronTrigger(hour='7'),  # 10 p.m. in KTS
    },
    "US": {
        "name": "US",
        "trigger": CronTrigger(hour='12'),  # 10 p.m. in KTS
    },
}

GITHUB_ISSUE_TITLE = "[GTRP] Google Trend Report ({TARGET_DATE})"
GITHUB_ISSUE_BODY = f"""
In time for each country at 10 p.m., Google Trend Keyword Report will be published with this issue comment.
- Korea
- France
- Swiss
- UK (United Kingdom)
- US (United States of America)
"""
