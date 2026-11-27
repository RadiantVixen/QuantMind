
def analysis_gate(state):
    errors = []

    for field in [
        "market_error",
        "risk_error",
        "news_error",
        "quant_error",
    ]:
        error = state.get(field)
        if error:
            errors.append(f"{field}: {error}")

    return {
        "analyst_errors": errors,
        "analysis_status": "READY",
    }


def route_after_analysis(state):
    # Market prediction and risk assessment are essential.
    if state.get("market_error") or state.get("risk_error"):
        return "failed"

    return "continue"


def analysis_error(state):
    errors = state.get("analyst_errors", [])

    return {
        "analysis_status": "FAILED",
        "analysis_error": (
            "Essential analyst failed. " + "; ".join(errors)
        ),
    }
