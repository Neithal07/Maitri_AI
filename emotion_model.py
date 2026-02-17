from deepface import DeepFace

def analyze_emotion(frame):
    result = DeepFace.analyze(
        frame,
        actions=["emotion"],
        enforce_detection=False
    )

    emotion = result[0]["dominant_emotion"]
    confidence = max(result[0]["emotion"].values())

    return {
        "emotion": emotion,
        "confidence": round(confidence, 3)
    }
