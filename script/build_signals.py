import pandas as pd
import feedparser
from datetime import datetime
from pytrends.request import TrendReq
import json
from pathlib import Path

signals = []

# -----------------
# SUBSTACK
# -----------------
SUBSTACKS = {
    "culture": "https://annehelen.substack.com/feed",
    "lifestyle": "https://heated.world/feed",
    "fashion": "https://blackbirdspyplane.substack.com/feed",
    "tech_culture": "https://platformer.news/feed"
}

for category, feed_url in SUBSTACKS.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:20]:
        signals.append({
            "date": entry.get("published", ""),
            "platform": "substack",
            "category": category,
            "type": "essay",
            "text": entry.title,
            "url": entry.link
        })

# -----------------
# GOOGLE TRENDS
# -----------------
pytrends = TrendReq(hl="en-US", tz=360)

KEYWORDS = [
    "cozy minimalism",
    "craft decor",
    "slow living home",
    "low tox beauty",
    "analog hobbies"
]

for kw in KEYWORDS:
    pytrends.build_payload([kw], timeframe="today 12-m")
    data = pytrends.interest_over_time()
    if not data.empty:
        signals.append({
            "date": datetime.now().isoformat(),
            "platform": "google_trends",
            "category": "mixed",
            "type": "search",
            "text": kw,
            "url": "https://trends.google.com"
        })

# -----------------
# NEWS
# -----------------
NEWS = {
    "design": "https://www.dezeen.com/feed/",
    "fashion": "https://www.voguebusiness.com/rss",
    "culture": "https://www.thecut.com/rss"
}

for category, feed_url in NEWS.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:20]:
        signals.append({
            "date": entry.get("published", ""),
            "platform": "news",
            "category": category,
            "type": "article",
            "text": entry.title,
            "url": entry.link
        })

# -----------------
# SAVE JSON
# -----------------
Path("data").mkdir(exist_ok=True)

with open("data/all_signals.json", "w", encoding="utf-8") as f:
    json.dump(signals, f, ensure_ascii=False, indent=2)

print("Signals updated:", len(signals))
