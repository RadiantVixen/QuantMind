import pandas as pd


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create the next-candle direction target."""

    df = df.copy()

    next_close = df["close"].shift(-1)

    df["target"] = (
        next_close > df["close"]
    ).astype(int)

    # The last row has no next candle.
    df = df.iloc[:-1]

    return df.reset_index(drop=True)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare raw market data for feature engineering."""

    df = df.copy()

    # Ensure chronological order
    df = df.sort_values("timestamp")

    # Remove duplicate timestamps
    df = df.drop_duplicates(
        subset=["timestamp"],
        keep="last",
    )

    # Create target
    df = create_target(df)

    return df.reset_index(drop=True)
