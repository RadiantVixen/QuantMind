def decision_analyst(state: dict) -> dict:
    prediction = state["prediction"]
    probability_up = state["probability_up"]
    risk_level = state["risk_level"]

    if risk_level == "HIGH":
        decision = "HOLD"
        reason = "Market risk is too high."

    elif prediction == "UP" and probability_up >= 0.55:
        decision = "BUY"
        reason = "The model predicts upward movement with sufficient probability."

    elif prediction == "DOWN" and probability_up <= 0.45:
        decision = "AVOID"
        reason = "The model predicts downward movement."

    else:
        decision = "HOLD"
        reason = "The model signal is not sufficiently strong."

    explanation = (
        f"Decision: {decision}. "
        f"Prediction: {prediction}. "
        f"Probability UP: {probability_up:.2%}. "
        f"Risk level: {risk_level}. "
        f"Reason: {reason}"
    )

    return {
        "decision": decision,
        "explanation": explanation,
    }


