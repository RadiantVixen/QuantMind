from typing import TypedDict, Optional


class QuantMindState(TypedDict, total=False):
    # Market configuration
    symbol: str
    timeframe: str

    # Quantitative model output
    latest_price: float
    prediction: str
    probability_up: float
    probability_down: float

    # Analyst outputs
    market_analysis: str
    risk_analysis: str
    news_analysis: str

    # Final decision
    decision: str
    explanation: str

    # Error handling
    errors: list[str]

    news_sentiment: str
    news_articles: list[dict]

    risk_level: str
    annualized_volatility: float
    max_drawdown: float
    approval_status: str
