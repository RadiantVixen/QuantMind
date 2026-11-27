from intelligence.agents.rag.ingestion import ingest_news
from intelligence.agents.rag.vector_store import retrieve_articles
from intelligence.agents.rag.sentiment import classify_sentiment

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
    
    sentiment_scores = []

    for article in articles:
        text = f"{article.get('title', '')} {article.get('content', '')}"

        sentiment = classify_sentiment(text)

        article["sentiment"] = sentiment["sentiment"]
        article["sentiment_score"] = sentiment["score"]

        sentiment_scores.append(sentiment["score"])

    average_score = (
        sum(sentiment_scores) / len(sentiment_scores)
        if sentiment_scores else 0
    )

    if average_score > 0:
        overall_sentiment = "BULLISH"
    elif average_score < 0:
        overall_sentiment = "BEARISH"
    else:
        overall_sentiment = "NEUTRAL"

    # 3. Prepare evidence for the Decision Agent
    analysis = "\n".join(
        f"- {article['metadata']['title']}: "
        f"{article['content']}"
        for article in articles
    )

    return {
        "news_analysis": analysis,
        "news_articles": articles,
        "news_sentiment": overall_sentiment,
        "news_sentiment_score": average_score,
    }
