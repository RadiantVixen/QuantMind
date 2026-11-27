import pandas as pd

from intelligence.features.technical_indicators import (
    calculate_returns,
    calculate_moving_averages,
    calculate_volatility,
    calculate_volume_features,
)


FEATURE_COLUMNS = [
    "return_1",
    "return_3",
    "sma_ratio",
    "volatility_5",
    "volume_change",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = calculate_returns(df)
    df = calculate_moving_averages(df)
    df = calculate_volatility(df)
    df = calculate_volume_features(df)

    # Remove rows with insufficient historical data
    df = df.dropna(subset=FEATURE_COLUMNS)

    return df.reset_index(drop=True)
