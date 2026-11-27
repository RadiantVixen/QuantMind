from intelligence.agents.rag.sentiment import classify_sentiment

examples = [
    "Bitcoin surges as institutional adoption grows",
    "Crypto market crashes after regulatory ban",
    "Bitcoin price remains stable today",
    "Bitcoin did not rally after the announcement",
]

for text in examples:
    print(text)
    print(classify_sentiment(text))
    print("-" * 50)