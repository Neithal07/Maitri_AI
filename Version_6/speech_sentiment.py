from sentiment import get_sentiment

# ===== Mental state keywords (priority) =====

STRESS_WORDS = {
    "stress", "stressed", "pressure", "overwhelmed", "tense",
    "anxious", "burned", "burnt", "deadline", "workload"
}

FATIGUE_WORDS = {
    "tired", "exhausted", "sleepy", "drained", "fatigue",
    "worn", "weak", "no energy", "can't stay awake"
}

# ===== Emotion buckets =====

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


def contains_phrase(text, phrases):
    return any(p in text for p in phrases)


def get_speech_emotion(text):
    t = text.lower()

    sentiment, intensity = get_sentiment(text)

    # ===== Mental states FIRST =====
    if contains_phrase(t, FATIGUE_WORDS):
        return "fatigue", intensity

    if contains_phrase(t, STRESS_WORDS):
        return "stress", intensity

    words = set(t.split())

    # ===== Negative emotions =====
    if sentiment == "Negative":
        if words & ANGER_WORDS:
            return "anger", intensity
        if words & FEAR_WORDS:
            return "fear", intensity
        if words & SAD_WORDS:
            return "sad", intensity
        return "sad", intensity

    # ===== Positive emotions =====
    if sentiment == "Positive":
        if words & SURPRISE_WORDS:
            return "surprise", intensity
        if words & HAPPY_WORDS:
            return "happy", intensity
        return "happy", intensity

    return "neutral", intensity