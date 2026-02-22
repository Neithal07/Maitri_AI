from flask import Flask, render_template, request, jsonify
import cv2, os, csv
import numpy as np
import tensorflow as tf
from datetime import datetime
from groq import Groq
from multimodal_logger import log_event, log_alert
import speech_recognition as sr

from sentiment import get_sentiment
from logger import log_sentiment
from alert import send_alert


latest_face_emotion = "None"
latest_face_confidence = 0.0

# ================= SETUP =================

app = Flask(__name__)

client = Groq(api_key="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")


ALERT_THRESHOLD = "Negative"

# ================= FACE MODEL =================

interpreter = tf.lite.Interpreter(model_path="emotion_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

labels = ["anger", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= FACE LOG =================

FACE_LOG = "face_emotion_log.csv"

if not os.path.exists(FACE_LOG):
    with open(FACE_LOG, "w", newline="") as f:
        csv.writer(f).writerow(["time","emotion","confidence"])

def log_face(emotion, confidence):
    with open(FACE_LOG, "a", newline="") as f:
        csv.writer(f).writerow([datetime.now(), emotion, confidence])

# ================= ROUTES =================



@app.route("/")
def home():
    return render_template("index.html")


# ---------- CHATBOT + SENTIMENT ----------

@app.route("/chat", methods=["POST"])
def chat():

    user_input = request.json["message"]

    sentiment, intensity = get_sentiment(user_input)

    global latest_face_emotion, latest_face_confidence

    log_event(
        user_input,
        sentiment,
        intensity,
        latest_face_emotion,
        latest_face_confidence
    )

    if sentiment == "Negative":
        log_alert(user_input, intensity, latest_face_emotion)
        
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": 
             "You are a friendly emotionally aware assistant for an astronaut. Respond naturally like a human. Ensure that the response is not longer than 40 words"},
            {"role": "user", "content": user_input}
        ]
    )

    reply = completion.choices[0].message.content

    return jsonify({
        "response": reply,
        "sentiment": sentiment,
        "intensity": intensity
    })

@app.route("/speech", methods=["POST"])
def speech_to_text():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"})

    audio_file = request.files["audio"]
    audio_path = "temp_audio.wav"
    audio_file.save(audio_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except:
        return jsonify({"error": "Could not understand speech"})

    # ---- Reuse existing chat logic ----

    sentiment, intensity = get_sentiment(text)

    global latest_face_emotion, latest_face_confidence

    log_event(
        text,
        sentiment,
        intensity,
        latest_face_emotion,
        latest_face_confidence
    )

    if sentiment == "Negative":
        log_alert(text, intensity, latest_face_emotion)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content":
             "You are a friendly emotionally aware assistant for an astronaut. Respond naturally like a human."},
            {"role": "user", "content": text}
        ]
    )

    reply = completion.choices[0].message.content

    return jsonify({
        "transcript": text,
        "response": reply,
        "sentiment": sentiment,
        "intensity": intensity
    })

@app.route("/logs")
def view_logs():
    try:
        with open("emotion_logs.txt") as f:
            data = f.read()
    except:
        data = "No logs yet."
    return f"<pre>{data}</pre>"


@app.route("/alerts")
def view_alerts():
    try:
        with open("alerts.txt") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "No alerts yet."




# ---------- FACE EMOTION ----------

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"face_detected": False})

    img = np.frombuffer(request.files["image"].read(), np.uint8)
    frame = cv2.imdecode(img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return jsonify({"face_detected": False})

    x, y, w, h = faces[0]

    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (48,48))
    face = face / 255.0
    face = face.reshape(1,48,48,1).astype("float32")

    interpreter.set_tensor(input_details[0]['index'], face)
    interpreter.invoke()

    pred = interpreter.get_tensor(output_details[0]['index'])[0]

    emotion = labels[np.argmax(pred)]
    confidence = float(np.max(pred))

    global latest_face_emotion, latest_face_confidence

    latest_face_emotion = emotion
    latest_face_confidence = round(confidence,3)

    return jsonify({
        "face_detected": True,
        "emotion": emotion,
        "confidence": latest_face_confidence,
        "box": [int(x),int(y),int(w),int(h)]
    })


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
