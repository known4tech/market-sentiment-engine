# scripts/download_tickers.py
import yfinance as yf
import os
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL"]
os.makedirs("data", exist_ok=True)

for ticker in tickers:
    print(f"Downloading {ticker}...")
    df = yf.download(ticker, period="6mo", auto_adjust=True)
    
    # Keep only required columns and fix index
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.index.name = 'Date'
    
    # Save cleaned CSV
    df.to_csv(f"data/{ticker.lower()}.csv")
    
print("Download complete!")