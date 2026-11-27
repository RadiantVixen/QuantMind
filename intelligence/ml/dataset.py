from sklearn.model_selection import train_test_split
import pandas as pd

from intelligence.features.feature_pipeline import FEATURE_COLUMNS


def prepare_dataset(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS]
    y = df["target"]

    # Preserve chronological order: no shuffling
    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    return X_train, X_test, y_train, y_test
