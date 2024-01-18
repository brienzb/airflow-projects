import requests
from bs4 import BeautifulSoup

GOOGLE_TREND_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"

response = requests.get(GOOGLE_TREND_RSS_URL)

if response.status_code == 200:
    xml = response.content
    soup = BeautifulSoup(xml, "lxml")
    
    titles = soup.find_all("title")
    approx_traffics = soup.find_all("ht:approx_traffic")

    rank = 1
    for title, approx_traffic in zip(titles[1:], approx_traffics):
        print(f"{rank} | {title.text} | {approx_traffic.text}")
        rank += 1
else:
    print(response.status_code)
