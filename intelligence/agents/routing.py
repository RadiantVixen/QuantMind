def route_after_approval(state: dict) -> str:
    if state["approval_status"] == "APPROVED":
        return "approved"

    return "rejected"