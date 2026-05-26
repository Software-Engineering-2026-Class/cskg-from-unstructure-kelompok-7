import feedparser
from bs4 import BeautifulSoup
import redis
import json
import time
import requests

# --- Configuration ---
RSS_FEEDS = {
    # News
    "TheHackerNews": "http://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/",
    # Threat Research
    "Securelist": "https://securelist.com/feed/",
    "CheckPointResearch": "https://research.checkpoint.com/category/threat-research/feed/",
    # Threat Monitoring
    "SANS_ISC": "https://isc.sans.edu/rssfeed_full.xml",
    # Vendor Intelligence
    "FortiGuardLabs": "https://filestore.fortinet.com/fortiguard/rss/outbreakalert.xml",

}
MAX_ARTICLES_PER_FEED = 2
MAX_NVD_ARTICLES = 5

# Redis connection details
# We use 'redis' as the host name because it's the service name in docker-compose
R_HOST = "redis"
R_PORT = 6379
ARTICLES_QUEUE = "articles_queue"  # List to push new articles to
SEEN_URLS_SET = "seen_urls"  # Set to track duplicates


def clean_html(html_content):
    """Strips all HTML tags from a string."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def fetch_articles(feed_url, max_articles=5):
    """Fetches and cleans articles from an RSS feed."""
    print(f"Fetching articles from: {feed_url}")
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:max_articles]:
        articles.append(
            {
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "N/A"),
                "content": clean_html(entry.get("summary", "")),
            }
        )
    return articles

def fetch_nvd_cves(max_articles=5):
    """Fetches recent CVEs from the NVD REST API v2."""
    print("Fetching articles from: NVD API (NIST)")
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    articles = []
    try:
        response = requests.get(url, params={"resultsPerPage": max_articles}, timeout=15)
        for item in response.json().get("vulnerabilities", []):
            cve = item.get("cve", {})
            cve_id = cve.get("id", "Unknown CVE")
            descriptions = cve.get("descriptions", [])
            description = next((d["value"] for d in descriptions if d.get("lang") == "en"), "N/A")
            articles.append(
                {
                    "title": cve_id,
                    "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                    "published": cve.get("published", "N/A"),
                    "content": f"Vulnerability: {cve_id}. Description: {description}",
                }
            )
    except Exception as e:
        print(f"NVD fetch failed: {e}")
    return articles

def connect_to_redis():
    """Connects to Redis with retries."""
    while True:
        try:
            r = redis.Redis(host=R_HOST, port=R_PORT, decode_responses=True)
            r.ping()
            print("Producer connected to Redis.")
            return r
        except redis.ConnectionError as e:
            print(f"Producer waiting for Redis... ({e})")
            time.sleep(5)


def run_producer():
    r = connect_to_redis()

    all_articles = []
    for _, url in RSS_FEEDS.items():
        all_articles.extend(fetch_articles(url, MAX_ARTICLES_PER_FEED))
    all_articles.extend(fetch_nvd_cves(MAX_NVD_ARTICLES))

    new_articles_pushed = 0
    for article in all_articles:
        # Check if this URL is already in our 'seen' set
        if not r.sismember(SEEN_URLS_SET, article["link"]):
            # If not, add it to the queue and the set
            article_json = json.dumps(article)
            r.rpush(ARTICLES_QUEUE, article_json)
            r.sadd(SEEN_URLS_SET, article["link"])

            new_articles_pushed += 1
            print(f"  [PRODUCER] Found new article: {article['title']}")

    print(
        f"Producer run complete. Pushed {new_articles_pushed} new articles to '{ARTICLES_QUEUE}'."
    )


if __name__ == "__main__":
    run_producer()
