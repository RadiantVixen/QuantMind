from langgraph.types import interrupt


def approval_node(state: dict) -> dict:
    decision = state["decision"]

    approved = interrupt({
        "message": "Human approval required",
        "proposed_decision": decision,
        "prediction": state["prediction"],
        "risk": state["risk_level"],
    })

    return {
        "approval_status": "APPROVED" if approved else "REJECTED"
    }

