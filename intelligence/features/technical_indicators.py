import pandas as pd


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["return_1"] = df["close"].pct_change(1)
    df["return_3"] = df["close"].pct_change(3)

    return df


def calculate_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["sma_5"] = df["close"].rolling(5).mean()
    df["sma_10"] = df["close"].rolling(10).mean()

    # Relative price position
    df["sma_ratio"] = df["sma_5"] / df["sma_10"] - 1

    return df


def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["volatility_5"] = (
        df["close"].pct_change().rolling(5).std()
    )

    return df


def calculate_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["volume_change"] = df["volume"].pct_change()

    return df
