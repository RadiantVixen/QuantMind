
def portfolio_manager(state):
    portfolio_value = state.get("portfolio_value", 10000.0)
    risk_per_trade_pct = state.get("risk_per_trade_pct", 1.0)
    stop_loss_pct = state.get("stop_loss_pct", 2.0)
    max_exposure_pct = state.get("max_exposure_pct", 20.0)
    current_exposure_pct = state.get("current_exposure_pct", 0.0)

    latest_price = state["latest_price"]
    decision = state["decision"]
    risk_level = state["risk_level"]

    # Validate inputs.
    if portfolio_value <= 0:
        raise ValueError("Portfolio value must be positive.")

    if not 0 < risk_per_trade_pct <= 100:
        raise ValueError("Risk per trade must be between 0 and 100.")

    if not 0 < stop_loss_pct <= 100:
        raise ValueError("Stop-loss percentage must be between 0 and 100.")

    if not 0 <= current_exposure_pct <= 100:
        raise ValueError("Current exposure must be between 0 and 100.")

    # Calculate the maximum amount we are willing to lose.
    risk_budget = portfolio_value * risk_per_trade_pct / 100

    # Calculate position size based on the stop-loss distance.
    position_value = risk_budget / (stop_loss_pct / 100)

    # Apply the portfolio exposure limit.
    max_position_value = portfolio_value * max_exposure_pct / 100

    remaining_exposure = (
        portfolio_value * max_exposure_pct / 100
        - portfolio_value * current_exposure_pct / 100
    )

    available_exposure = max(0, remaining_exposure)

    position_value = min(
        position_value,
        max_position_value,
        available_exposure,
    )

    # No new position if the decision or risk level prohibits it.
    if decision != "BUY" or risk_level == "HIGH":
        position_value = 0.0

    estimated_loss = position_value * stop_loss_pct / 100
    position_units = position_value / latest_price

    return {
        "risk_budget": round(risk_budget, 2),
        "recommended_position_value": round(position_value, 2),
        "recommended_position_units": round(position_units, 8),
        "estimated_max_loss": round(estimated_loss, 2),
        "portfolio_exposure_after_trade_pct": round(
            current_exposure_pct + position_value / portfolio_value * 100,
            2,
        ),
    }
