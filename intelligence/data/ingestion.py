
import pandas as pd

from intelligence.data.providers.binance import fetch_ohlcv


REQUIRED_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def ingest_market_data(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    limit: int = 500,
) -> pd.DataFrame:
    """Fetch and validate market data."""

    # 1. Fetch
    df = fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
    )

    # 2. Validate schema
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # 3. Remove duplicate timestamps
    df = df.drop_duplicates(
        subset=["timestamp"],
        keep="last",
    )

    # 4. Sort chronologically
    df = df.sort_values("timestamp")

    # 5. Validate numerical values
    numeric_columns = [
        "open", "high", "low", "close", "volume"
    ]

    if df[numeric_columns].isnull().any().any():
        raise ValueError("Missing numerical values.")

    if not (df[numeric_columns] >= 0).all().all():
        raise ValueError("Negative market values detected.")

    # 6. Validate OHLC consistency
    if (df["high"] < df[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("Invalid high prices.")

    if (df["low"] > df[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("Invalid low prices.")

    return df.reset_index(drop=True)
