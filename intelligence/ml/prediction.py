
import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).with_name("model.joblib")


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Train the model first."
        )

    return joblib.load(MODEL_PATH)


def predict_direction(features: pd.DataFrame) -> dict:
    model = load_model()

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    return {
        "direction": "UP" if prediction == 1 else "DOWN",
        "probability_up": float(probabilities[1]),
        "probability_down": float(probabilities[0]),
    }
