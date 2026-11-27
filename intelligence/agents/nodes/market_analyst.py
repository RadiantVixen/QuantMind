from intelligence.data.ingestion import ingest_market_data
from intelligence.data.preprocessing import prepare_data
from intelligence.features.feature_pipeline import (
    build_features,
    FEATURE_COLUMNS,
)
from intelligence.ml.prediction import predict_direction


def market_analyst(state: dict) -> dict:
    # 1. Fetch market data
    df = ingest_market_data(
        symbol=state.get("symbol", "BTC/USDT"),
        timeframe=state.get("timeframe", "1h"),
    )

    # 2. Prepare data and calculate features
    df = prepare_data(df)
    df = build_features(df)

    # 3. Extract latest features
    latest_features = df[FEATURE_COLUMNS].iloc[[-1]]

    # 4. Run the ML model
    result = predict_direction(latest_features)

    # 5. Update LangGraph State
    return {
        "latest_price": float(df["close"].iloc[-1]),
        "prediction": result["direction"],
        "probability_up": result["probability_up"],
        "probability_down": result["probability_down"],
    }
