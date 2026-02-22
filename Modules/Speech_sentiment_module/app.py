from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

from sentiment import get_sentiment
from logger import log_sentiment
from alert import send_alert

THRESHOLD = 0.5

app = Flask(__name__)

client = Groq(api_key="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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    text = request.json["message"]
    
    sentiment, intensity = get_sentiment(text)

    log_sentiment(text, sentiment, intensity)

    if intensity > THRESHOLD:
        send_alert(text, intensity)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a friendly emotionally aware assistant for an astronaut. Respond naturally. Donot let them know you are an LLM, act human"},
            {"role": "user", "content": text}

        ]
    )

    reply = completion.choices[0].message.content

    return jsonify({
        "response": reply,
        "sentiment": sentiment,
        "intensity": intensity
    })

@app.route("/logs")
def view_logs():
    try:
        with open("sentiment_logs.txt") as f:
            data = f.read()
    except:
        data = "No logs yet"

    return "<pre>" + data + "</pre>"

if __name__ == "__main__":
    app.run(debug=True)
