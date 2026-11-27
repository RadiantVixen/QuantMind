from langgraph.types import interrupt


def approval_node(state):
    response = interrupt({
        "message": "Human approval required",
        "proposed_decision": state["decision"],
        "decision_score": state["decision_score"],
        "prediction": state["prediction"],
        "risk_level": state["risk_level"],
        "recommended_position_value": state["recommended_position_value"],
        "estimated_max_loss": state["estimated_max_loss"],
    })

    approved = (
        response.get("approved", False)
        if isinstance(response, dict)
        else bool(response)
    )

    return {
        "approval_status": "APPROVED" if approved else "REJECTED"
    }
