# scripts/visualize.py
import matplotlib.pyplot as plt

def plot_data(df, ticker):
    """
    Plots the Close price and moving averages for the given ticker.
    Saves the plot as an image in the 'plots' folder.
    """
    import os
    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue')

    # Optional: Plot 20-day and 50-day moving averages if present
    if 'MA20' in df.columns:
        plt.plot(df.index, df['MA20'], label='20-Day MA', color='orange')
    if 'MA50' in df.columns:
        plt.plot(df.index, df['MA50'], label='50-Day MA', color='green')

    plt.title(f"{ticker} Price Chart")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"plots/{ticker.lower()}_plot.png")
    plt.close()