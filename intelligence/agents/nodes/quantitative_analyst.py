
import numpy as np
from intelligence.data.ingestion import ingest_market_data


def quantitative_analyst(state):
    symbol = state.get("symbol", "BTC/USDT")
    timeframe = state.get("timeframe", "1h")

    df = ingest_market_data(
        symbol=symbol,
        timeframe=timeframe,
        limit=200,
    )

    if len(df) < 60:
        raise ValueError("Not enough candles for quantitative analysis.")

    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    # 1. Trend: Exponential Moving Averages
    ema_20 = close.ewm(span=20, adjust=False).mean()
    ema_50 = close.ewm(span=50, adjust=False).mean()

    if ema_20.iloc[-1] > ema_50.iloc[-1]:
        trend = "BULLISH"
    elif ema_20.iloc[-1] < ema_50.iloc[-1]:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"

    # 2. Momentum: RSI (14)
    delta = close.diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.ewm(
        alpha=1 / 14, min_periods=14, adjust=False
    ).mean()

    avg_loss = losses.ewm(
        alpha=1 / 14, min_periods=14, adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    latest_rsi = float(rsi.iloc[-1])

    if latest_rsi >= 70:
        momentum = "OVERBOUGHT"
    elif latest_rsi <= 30:
        momentum = "OVERSOLD"
    else:
        momentum = "NEUTRAL"

    # 3. Volatility regime
    returns = close.pct_change()

    rolling_volatility = returns.rolling(20).std()
    historical_volatility = rolling_volatility.dropna()

    current_volatility = float(historical_volatility.iloc[-1])
    median_volatility = float(historical_volatility.median())

    if current_volatility > median_volatility * 1.5:
        volatility_regime = "HIGH"
    elif current_volatility < median_volatility * 0.5:
        volatility_regime = "LOW"
    else:
        volatility_regime = "NORMAL"

    # 4. Support and resistance (previous 20 candles)
    support = float(low.iloc[-21:-1].min())
    resistance = float(high.iloc[-21:-1].max())

    latest_price = float(close.iloc[-1])

    analysis = (
        f"Trend: {trend}. "
        f"RSI: {latest_rsi:.2f} ({momentum}). "
        f"Volatility regime: {volatility_regime}. "
        f"Recent support: {support:.2f}. "
        f"Recent resistance: {resistance:.2f}."
    )

    return {
        "quant_trend": trend,
        "quant_rsi": round(latest_rsi, 2),
        "quant_momentum": momentum,
        "quant_volatility_regime": volatility_regime,
        "quant_support": round(support, 2),
        "quant_resistance": round(resistance, 2),
        "quant_analysis": analysis,
    }
