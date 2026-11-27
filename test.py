from intelligence.data.ingestion import ingest_market_data
from intelligence.data.preprocessing import prepare_data
from intelligence.features.feature_pipeline import build_features, FEATURE_COLUMNS

df = ingest_market_data()
df = prepare_data(df)
df = build_features(df)

print(df[FEATURE_COLUMNS].tail())
print("\nFeature shape:", df[FEATURE_COLUMNS].shape)
print("\nMissing values:\n", df[FEATURE_COLUMNS].isnull().sum())


from intelligence.ml.backtesting import (
    backtest,
    calculate_performance,
)

predictions = model.predict(X_test)

test_df = df.loc[X_test.index].copy()

results = backtest(test_df, predictions)

performance = calculate_performance(results)

print("\nBACKTEST RESULTS")
for metric, value in performance.items():
    print(f"{metric}: {value:.4f}")
