from intelligence.agents.graph import build_graph

app = build_graph()

initial_state = {
    "symbol": "BTC/USDT",
    "timeframe": "1h",
}

result = app.invoke(initial_state)

print("\n========== QUANTMIND ==========")
print("Symbol:", result["symbol"])
print("Price:", result["latest_price"])
print("Prediction:", result["prediction"])
print("Probability UP:", result["probability_up"])
print("Risk:", result["risk_analysis"])
print("News:", result["news_analysis"])
print("\nFINAL DECISION:", result["decision"])
print(result["explanation"])