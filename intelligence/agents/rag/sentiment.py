POSITIVE_WORDS = {
    "surge": 2,
    "rally": 2,
    "bullish": 2,
    "gain": 1,
    "growth": 1,
    "adoption": 1,
    "approval": 2,
    "突破": 1,
    "recovery": 1,
    "record": 1,
    "rise": 1,
    "rises": 1,
    "上涨": 1,
    "upgrade": 1,
    "inflow": 1,
}

NEGATIVE_WORDS = {
    "crash": 2,
    "collapse": 2,
    "bearish": 2,
    "plunge": 2,
    "decline": 1,
    "loss": 1,
    "hack": 2,
    "ban": 2,
    "lawsuit": 1,
    "risk": 1,
    "warning": 1,
    "selloff": 2,
    "drop": 1,
    "drops": 1,
    "outflow": 1,
    "liquidation": 2,
}

NEGATIONS = {"not", "no", "never", "without", "fails", "failed"}

def classify_sentiment(text: str) -> dict:
    words = text.lower().split()

    score = 0
    for i, word in enumerate(words):
        word = word.strip(".,!?;:\"'()[]{}")

        value = POSITIVE_WORDS.get(word, 0) - NEGATIVE_WORDS.get(word, 0)

        # Basic negation handling: check the previous two words.
        previous_words = words[max(0, i - 2):i]
        if any(w.strip(".,!?;:\"'()[]{}") in NEGATIONS for w in previous_words):
            value *= -1

        score += value

    if score > 0:
        label = "BULLISH"
    elif score < 0:
        label = "BEARISH"
    else:
        label = "NEUTRAL"

    return {
        "sentiment": label,
        "score": score,
    }