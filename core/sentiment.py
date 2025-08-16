# core/sentiment.py (UPGRADED)
import pandas as pd

def calculate_asset_specific_sentiment(df: pd.DataFrame, window_size=7):
    if df.empty or 'assets' not in df.columns:
        return {}

    # Group by each mapped asset and calculate its rolling sentiment
    sentiment_by_asset = {}
    for asset_name, group in df.groupby('assets'):
        group = group.set_index('published').sort_index()
        daily_sentiment = group['sentiment'].resample('D').mean().ffill()
        sentiment_by_asset[asset_name] = daily_sentiment.rolling(window=f"{window_size}D").mean()

    return sentiment_by_asset