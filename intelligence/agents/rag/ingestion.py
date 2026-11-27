
import feedparser
import re
from html.parser import HTMLParser

from intelligence.agents.rag.vector_store import store_articles


NEWS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]


class HTMLTextExtractor(HTMLParser):
    """Extract readable text from HTML content."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip_content = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip_content = False

    def handle_data(self, data):
        if not self.skip_content:
            self.text_parts.append(data)


def clean_text(raw_text):
    if not raw_text:
        return ""

    parser = HTMLTextExtractor()
    parser.feed(raw_text)

    text = " ".join(parser.text_parts)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def fetch_news(limit=30):
    articles = []
    seen_links = set()
    seen_titles = set()

    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = clean_text(entry.get("title", ""))
            summary = clean_text(
                entry.get("summary", entry.get("description", ""))
            )
            link = entry.get("link", "")

            normalized_title = title.lower()

            if not title or not link:
                continue

            if link in seen_links or normalized_title in seen_titles:
                continue

            seen_links.add(link)
            seen_titles.add(normalized_title)

            articles.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": entry.get(
                    "published",
                    entry.get("updated", "")
                ),
            })

            if len(articles) >= limit:
                return articles

    return articles


def ingest_news():
    articles = fetch_news()

    if not articles:
        return 0

    store_articles(articles)

    return len(articles)
