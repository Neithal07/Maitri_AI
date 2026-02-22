import requests
from datetime import datetime

EARTH_SERVER = "http://10.12.8.64:8000/alert"

def send_alert(text, intensity):
    payload = {
        "text": text,
        "intensity": intensity,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    requests.post(EARTH_SERVER, json=payload)
