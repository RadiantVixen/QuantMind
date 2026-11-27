
import feedparser

from intelligence.agents.rag.vector_store import store_articles


NEWS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]


def fetch_news(limit: int = 30) -> list[dict]:
    articles = []

    for url in NEWS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            })

    unique = {
        article["link"]: article
        for article in articles
        if article["link"]
    }

    return list(unique.values())[:limit]


def ingest_news():
    articles = fetch_news()
    store_articles(articles)

    return len(articles)

