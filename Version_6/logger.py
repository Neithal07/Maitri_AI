from datetime import datetime

LOG_FILE = "sentiment_logs.txt"

def log_sentiment(text, sentiment, intensity):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {text} | {sentiment} | {intensity}\n")
