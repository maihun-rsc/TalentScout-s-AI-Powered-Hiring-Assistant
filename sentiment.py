from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment polarity and label.
    Polarity: -1 (negative) to +1 (positive)
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        label = "Positive 😊"
        color = "green"
    elif polarity < -0.1:
        label = "Negative 😟"
        color = "red"
    else:
        label = "Neutral 😐"
        color = "gray"

    return {
        "polarity": round(polarity, 2),
        "label": label,
        "color": color
    }
