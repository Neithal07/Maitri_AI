from flask import Flask, jsonify
from camera import get_frame
from emotion_model import analyze_emotion

app = Flask(__name__)

@app.route("/face-emotion", methods=["GET"])
def face_emotion():
    frame = get_frame()
    result = analyze_emotion(frame)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
