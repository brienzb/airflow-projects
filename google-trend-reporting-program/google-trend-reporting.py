import html
import pprint
import re
import requests
import unicodedata

from bs4 import BeautifulSoup
from bs4.element import Tag


GOOGLE_TREND_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo={GEOGRAPHY}"
GEOGRAPHY_LIST = ["KR", "US"]


def parse_google_trend_keyword(item: Tag):
    def _decoded_tag(tag: Tag):
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
    soup = BeautifulSoup(xml, "lxml")
    
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


google_trend_keywords = get_google_trend_keywords("KR")
pprint.pprint(google_trend_keywords)
