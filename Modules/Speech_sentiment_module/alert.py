import requests
from datetime import datetime

EARTH_SERVER = "http://127.0.0.1:8000/alert"

def send_alert(text, intensity):
    payload = {
        "text": text,
        "intensity": intensity,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    try:
        requests.post(EARTH_SERVER, json=payload, timeout=2)
    except:
        print("⚠ Alert server not reachable")
