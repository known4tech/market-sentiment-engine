# core/nlp.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create a single, reusable analyzer object
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    """
    Analyzes the sentiment of a given text.

    Args:
        text (str): The text to analyze (e.g., a news headline).

    Returns:
        float: The compound sentiment score, from -1 (most negative) to +1 (most positive).
    """
    # The polarity_scores() method returns a dictionary.
    # We are interested in the 'compound' score.
    scores = analyzer.polarity_scores(text)
    return scores['compound']

# This part allows you to run this file directly to test it
if __name__ == "__main__":
    print("--- Testing Sentiment Analyzer ---")

    positive_headline = "Stocks Surge to Record Highs on Strong Economic Data"
    negative_headline = "Market Plummets Amidst Fears of Inflation and Rate Hikes"
    neutral_headline = "The FTSE 100 Index Closed at 7,500 Points"

    pos_score = get_sentiment_score(positive_headline)
    neg_score = get_sentiment_score(negative_headline)
    neu_score = get_sentiment_score(neutral_headline)

    print(f"'{positive_headline}' | Score: {pos_score}")
    print(f"'{negative_headline}' | Score: {neg_score}")
    print(f"'{neutral_headline}' | Score: {neu_score}")