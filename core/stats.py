# core/stats.py
import pandas as pd
import numpy as np

def generate_signals(price_df: pd.DataFrame, sentiment_series: pd.Series):
    """
    Analyzes price and sentiment to generate a summary and a trading signal.
    """
    if price_df.empty or len(price_df) < 2 or sentiment_series is None or sentiment_series.empty:
        return {}

    # --- FIX: Use .iloc[-1].item() to extract the value as a standard Python float ---
    latest_price = price_df['close'].iloc[-1].item()
    previous_price = price_df['close'].iloc[-2].item()

    # --- Key Metrics ---
    price_change = latest_price - previous_price
    price_pct_change = (price_change / previous_price) * 100

    latest_sentiment = sentiment_series.iloc[-1]

    # --- Signal Generation ---
    sentiment_mean = sentiment_series.mean()
    sentiment_std = sentiment_series.std()

    if sentiment_std > 0:
        z_score = (latest_sentiment - sentiment_mean) / sentiment_std
    else:
        z_score = 0

    signal = "Neutral 😐"
    recommendation = "Sentiment is within its normal range. Market conditions appear stable."

    if z_score > 1.5:
        signal = "Strong Buy 🟢"
        recommendation = "Sentiment is significantly positive compared to its recent average, suggesting strong upward momentum."
    elif z_score > 0.5:
        signal = "Buy 🔼"
        recommendation = "Sentiment is moderately positive, suggesting favorable conditions."
    elif z_score < -1.5:
        signal = "Strong Sell 🔴"
        recommendation = "Sentiment is significantly negative compared to its recent average, suggesting strong downward pressure."
    elif z_score < -0.5:
        signal = "Sell 🔽"
        recommendation = "Sentiment is moderately negative, suggesting unfavorable conditions."

    return {
        "latest_price": f"{latest_price:,.2f}",
        "price_change": f"{price_change:,.2f}",
        "price_pct_change": f"{price_pct_change:.2f}%",
        "latest_sentiment": f"{latest_sentiment:.2f}",
        "sentiment_z_score": f"{z_score:.2f}",
        "signal": signal,
        "recommendation": recommendation
    }