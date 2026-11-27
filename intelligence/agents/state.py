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
    quant_analysis: str

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

    news_sentiment_score: float
    portfolio_value: float
    risk_per_trade_pct: float
    stop_loss_pct: float
    max_exposure_pct: float
    current_exposure_pct: float

    risk_budget: float
    recommended_position_value: float
    recommended_position_units: float
    estimated_max_loss: float
    portfolio_exposure_after_trade_pct: float

    quant_trend: str
    quant_rsi: float
    quant_momentum: str
    quant_volatility_regime: str
    quant_support: float
    quant_resistance: float
    quant_analysis: str
    decision_score: float
    analyst_agreement: str
    market_error: str
    risk_error: str
    news_error: str
    quant_error: str

    analyst_errors: list[str]
    analysis_status: str
    analysis_error: str