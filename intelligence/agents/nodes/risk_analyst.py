import numpy as np

from intelligence.data.ingestion import ingest_market_data


def risk_analyst(state: dict) -> dict:
    # 1. Fetch recent market data
    df = ingest_market_data(
        symbol=state.get("symbol", "BTC/USDT"),
        timeframe=state.get("timeframe", "1h"),
        limit=100,
    )

    # 2. Calculate hourly returns
    returns = df["close"].pct_change().dropna()

    # 3. Calculate annualized volatility
    volatility = returns.std() * np.sqrt(24 * 365)

    # 4. Calculate maximum drawdown
    rolling_peak = df["close"].cummax()
    drawdowns = df["close"] / rolling_peak - 1
    max_drawdown = drawdowns.min()

    # 5. Classify risk (illustrative thresholds)
    if volatility < 0.5:
        risk_level = "LOW"
    elif volatility < 1.0:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    analysis = (
        f"Risk level: {risk_level}. "
        f"Annualized volatility: {volatility:.2%}. "
        f"Maximum drawdown over observation window: {max_drawdown:.2%}."
    )


    return {
        "risk_level": risk_level,
        "annualized_volatility": float(volatility),
        "max_drawdown": float(max_drawdown),
        "risk_analysis": analysis,
    }