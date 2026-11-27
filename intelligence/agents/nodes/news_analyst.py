from intelligence.agents.rag.ingestion import ingest_news
from intelligence.agents.rag.vector_store import retrieve_articles


def news_analyst(state: dict) -> dict:

    # 1. Fetch and index new articles
    ingested_count = ingest_news()

    # 2. Retrieve semantically relevant news
    symbol = state.get("symbol", "BTC/USDT")
    asset = symbol.split("/")[0]

    query = (
        f"Recent news about {asset}, cryptocurrency market "
        "developments, price movements, regulation, adoption, "
        "institutional investment and market risks."
    )

    articles = retrieve_articles(query, top_k=5)

    # 3. Prepare evidence for the Decision Agent
    analysis = "\n".join(
        f"- {article['metadata']['title']}: "
        f"{article['content']}"
        for article in articles
    )

    return {
        "news_analysis": analysis or "No relevant news retrieved.",
        "news_articles": articles,
    }
