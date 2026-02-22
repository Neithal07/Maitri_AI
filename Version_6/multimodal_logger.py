from datetime import datetime

LOG_FILE = "emotion_logs.txt"
ALERT_FILE = "alerts.txt"

def log_event(text, text_sent, intensity, face_emotion, face_conf):

    with open(LOG_FILE, "a") as f:
        f.write(
            f"{datetime.now()} | {text} | {text_sent} | {intensity} | "
            f"{face_emotion} | {face_conf}\n"
        )


def log_alert(text, intensity, face_emotion):

    with open(ALERT_FILE, "a") as f:
        f.write(
            f"{datetime.now()} | {text} | {intensity} | {face_emotion}\n"
        )
