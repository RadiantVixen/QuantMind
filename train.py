from intelligence.data.ingestion import ingest_market_data
from intelligence.data.preprocessing import prepare_data
from intelligence.features.feature_pipeline import build_features
from intelligence.ml.dataset import prepare_dataset
from intelligence.ml.training import train_model
from intelligence.ml.evaluation import evaluate_model

df = ingest_market_data()
df = prepare_data(df)
df = build_features(df)

X_train, X_test, y_train, y_test = prepare_dataset(df)

model = train_model(X_train, y_train)

evaluate_model(model, X_train, y_train, X_test, y_test)
