# scripts/metrics.py
def add_metrics(df):
    """
    Adds common trading metrics:
    - 20-day and 50-day moving averages
    - Daily returns
    """
    if 'Close' not in df.columns:
        raise ValueError("DataFrame must have 'Close' column to calculate metrics")

    # Moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # Daily returns
    df['Daily_Return'] = df['Close'].pct_change()

    return df