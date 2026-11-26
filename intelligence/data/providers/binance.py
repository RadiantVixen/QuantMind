import ccxt
import pandas as pd


def fetch_ohlcv(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    limit: int = 500,
) -> pd.DataFrame:
    """Fetch historical OHLCV candles from Binance."""

    exchange = ccxt.binance({
        "enableRateLimit": True,
    })

    candles = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
    )

    if not candles:
        raise ValueError("No market data returned.")

    df = pd.DataFrame(
        candles,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], unit="ms", utc=True
    )

    numeric_columns = [
        "open", "high", "low", "close", "volume"
    ]
    df[numeric_columns] = df[numeric_columns].astype(float)

    if df.isnull().any().any():
        raise ValueError("Market data contains missing values.")

    return df
