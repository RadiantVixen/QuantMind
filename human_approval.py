from langgraph.types import Command
from langgraph.checkpoint.sqlite import SqliteSaver

from intelligence.agents.graph import build_graph

config = {
    "configurable": {
        "thread_id": "approval-test-005"
    }
}

with SqliteSaver.from_conn_string("quantmind_checkpoints.sqlite") as checkpointer:

    app = build_graph(checkpointer=checkpointer)

    initial_state = {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
    }

    result = app.invoke(initial_state, config=config)

    print("Proposed decision:", result["decision"])

    # The graph is paused here.
    approval = input("Approve this decision? (yes/no): ").lower() == "yes"

    result = app.invoke(
        Command(resume=approval),
        config=config,
    )

    print("Approval status:", result["approval_status"])