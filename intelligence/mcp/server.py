from mcp.server import MCPServer
from intelligence.agents.nodes.market_analyst import market_analyst
from intelligence.agents.nodes.risk_analyst import risk_analyst
from intelligence.agents.rag.ingestion import ingest_news
from intelligence.agents.rag.vector_store import retrieve_articles


mcp = MCPServer("QuantMind")


@mcp.tool()
def get_market_prediction(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
) -> dict:
    """Get the ML-based market direction prediction."""

    return market_analyst({
        "symbol": symbol,
        "timeframe": timeframe,
    })


@mcp.tool()
def get_risk_assessment(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
) -> dict:
    """Calculate market volatility and drawdown risk."""

    return risk_analyst({
        "symbol": symbol,
        "timeframe": timeframe,
    })


@mcp.tool()
def search_crypto_news(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Retrieve semantically relevant cryptocurrency news."""

    ingest_news()

    return retrieve_articles(
        query=query,
        top_k=top_k,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
