from intelligence.agents.graph import build_graph

app = build_graph()

initial_state = {
    "symbol": "BTC/USDT",
    "timeframe": "1h",
}

for event in app.stream(
    initial_state,
    stream_mode="updates",
):
    for node_name, output in event.items():
        print(f"\n--- {node_name.upper()} ---")

        for key, value in output.items():
            if key == "news_articles":
                print(f"Retrieved {len(value)} articles")
            else:
                print(f"{key}: {value}")