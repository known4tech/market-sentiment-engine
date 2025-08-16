# scripts/preprocess.py
import pandas as pd  # <-- you were missing this
import numpy as np

def preprocess(df):
    # Drop any empty rows
    df = df.dropna(how='all')

    # Ensure numeric columns are correct
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values with forward fill
    df = df.fillna(method='ffill')

    # Add some basic features
    if 'Close' in df.columns:
        df['Daily Return'] = df['Close'].pct_change()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()

    return df