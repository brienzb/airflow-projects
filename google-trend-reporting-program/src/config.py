import os

from apscheduler.triggers.cron import CronTrigger


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
GEOGRAPHY_LIST =  ["KR", "US"]  # ["KR", "JP", "FR", "CH", "DE", "IT", "ES", "GB", "US", "CA"]
GEOGRAPHY_DICT = {
    "KR": {
        "trigger": CronTrigger(hour='22'),
        "next_run_date": None,
    },
    "US": {
        "trigger": CronTrigger(hour='12'),
        "next_run_date": None,
    },
}

LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
REPORT_DATE_FORMAT = "%Y-%m-%d"

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_PATH, "template")
