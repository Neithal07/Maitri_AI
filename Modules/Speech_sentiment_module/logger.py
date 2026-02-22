from datetime import datetime

def log_sentiment(text, sentiment, intensity):
    with open("sentiment_logs.txt", "a") as f:
        f.write(f"{datetime.now()} | {text} | {sentiment} | {intensity}\n")
