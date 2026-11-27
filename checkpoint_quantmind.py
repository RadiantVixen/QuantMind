from langgraph.checkpoint.sqlite import SqliteSaver
from intelligence.agents.graph import build_graph

initial_state = {
    "symbol": "BTC/USDT",
    "timeframe": "1h",
}

config = {
    "configurable": {
        "thread_id": "btc-analysis-001"
    }
}

with SqliteSaver.from_conn_string("quantmind_checkpoints.sqlite") as checkpointer:

    app = build_graph(checkpointer=checkpointer)

    result = app.invoke(initial_state, config=config)

    print("\nFINAL DECISION:", result["decision"])

    # Retrieve the saved state
    snapshot = app.get_state(config)

    print("\nSAVED STATE:")
    print("Thread ID:", snapshot.config["configurable"]["thread_id"])
    print("Decision:", snapshot.values["decision"])
    print("Prediction:", snapshot.values["prediction"])