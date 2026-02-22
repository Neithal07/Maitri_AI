from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# ===== Keyword buckets =====

HAPPY_WORDS = {
    "happy", "great", "awesome", "love", "excited", "amazing", "fantastic"
}

SURPRISE_WORDS = {
    "wow", "shocked", "unexpected", "surprised", "can't believe"
}

ANGER_WORDS = {
    "angry", "mad", "furious", "hate", "annoyed", "frustrated"
}

FEAR_WORDS = {
    "scared", "afraid", "worried", "nervous", "panic"
}

SAD_WORDS = {
    "sad", "cry", "lonely", "depressed", "upset", "down"
}

STRESS_WORDS = {
    "stress", "stressed", "pressure", "overwhelmed", "deadline", "workload"
}

FATIGUE_WORDS = {
    "tired", "exhausted", "sleepy", "drained", "fatigue", "no energy"
}


def contains_phrase(text, phrases):
    return any(p in text for p in phrases)


def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    t = text.lower()
    words = set(t.split())

    # ===== Derived states first =====
    if contains_phrase(t, FATIGUE_WORDS):
        return "fatigue", round(scores["neu"], 2)

    if contains_phrase(t, STRESS_WORDS):
        return "stress", round(scores["neg"], 2)

    # ===== Original sentiment logic preserved =====

    if compound >= 0.05:
        if words & SURPRISE_WORDS:
            return "surprise", round(scores["pos"], 2)
        return "happy", round(scores["pos"], 2)

    elif compound <= -0.05:
        if words & ANGER_WORDS:
            return "anger", round(scores["neg"], 2)
        if words & FEAR_WORDS:
            return "fear", round(scores["neg"], 2)
        return "sad", round(scores["neg"], 2)

    else:
        return "neutral", round(scores["neu"], 2)


# Standalone test unchanged structure
if __name__ == "__main__":
    print("Sentiment Analyzer (type 'exit' to quit)\n")

    while True:
        msg = input("Message: ")

        if msg.lower() == "exit":
            break

        sentiment, intensity = get_sentiment(msg)

        print("\nInput:", msg)
        print("Final sentiment:", sentiment)
        print("Intensity:", intensity)