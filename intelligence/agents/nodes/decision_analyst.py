
def decision_analyst(state):
    probability_up = state["probability_up"]
    risk_level = state["risk_level"]

    # 1. ML signal: convert probability into [-1, +1].
    ml_signal = (2 * probability_up) - 1

    # 2. Technical trend.
    trend = state.get("quant_trend", "NEUTRAL")

    trend_signal = {
        "BULLISH": 1,
        "BEARISH": -1,
        "NEUTRAL": 0,
    }.get(trend, 0)

    # 3. RSI momentum.
    rsi = state.get("quant_rsi", 50)

    if rsi >= 55:
        rsi_signal = 1
    elif rsi <= 45:
        rsi_signal = -1
    else:
        rsi_signal = 0

    # 4. News sentiment.
    news_sentiment = state.get("news_sentiment", "NEUTRAL")

    news_signal = {
        "BULLISH": 1,
        "BEARISH": -1,
        "NEUTRAL": 0,
    }.get(news_sentiment, 0)

    # Combine the four signals.
    decision_score = (
        0.50 * ml_signal
        + 0.20 * trend_signal
        + 0.15 * rsi_signal
        + 0.15 * news_signal
    )

    # Count directional agreement.
    signals = [ml_signal, trend_signal, rsi_signal, news_signal]

    bullish_votes = sum(signal > 0 for signal in signals)
    bearish_votes = sum(signal < 0 for signal in signals)

    if bullish_votes > bearish_votes:
        agreement = "BULLISH"
    elif bearish_votes > bullish_votes:
        agreement = "BEARISH"
    else:
        agreement = "MIXED"

    # Risk override.
    if risk_level == "HIGH":
        decision = "HOLD"
        reason = "High market risk overrides the directional signals."

    elif decision_score >= 0.25:
        decision = "BUY"
        reason = "The combined signals favor upward movement."

    elif decision_score <= -0.25:
        decision = "AVOID"
        reason = "The combined signals favor downward movement."

    else:
        decision = "HOLD"
        reason = "The analysts do not provide a sufficiently strong directional signal."

    explanation = (
        f"{reason} "
        f"ML signal: {ml_signal:.2f}. "
        f"Trend: {trend}. "
        f"RSI: {rsi:.2f}. "
        f"News: {news_sentiment}. "
        f"Analyst agreement: {agreement}. "
        f"Combined score: {decision_score:.3f}. "
        f"Risk: {risk_level}."
    )

    return {
        "decision": decision,
        "decision_score": round(decision_score, 3),
        "analyst_agreement": agreement,
        "explanation": explanation,
    }
