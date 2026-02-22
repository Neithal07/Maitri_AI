from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        return "Positive", round(scores["pos"], 2)
    elif compound <= -0.05:
        return "Negative", round(scores["neg"], 2)
    else:
        return "Neutral", round(scores["neu"], 2)

if __name__ == "__main__":
    while True:
        t = input("Text: ")
        print(get_sentiment(t))
