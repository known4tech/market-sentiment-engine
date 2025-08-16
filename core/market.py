# core/market.py
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

def fetch_price_data(ticker):
    """
    Fetches the last 90 days of daily price data for a given ticker using yfinance.
    """
    print(f"Fetching yfinance data for ticker: {ticker}...")
    try:
        # Define the date range (today and 90 days ago)
        today = date.today()
        ninety_days_ago = today - timedelta(days=90)
        
        # Download the data from yfinance
        df = yf.download(
            ticker,
            start=ninety_days_ago.strftime("%Y-%m-%d"),
            end=today.strftime("%Y-%m-%d"),
            auto_adjust=True # Automatically adjusts for splits and dividends
        )

        if df.empty:
            print(f"No yfinance data found for {ticker}.")
            return pd.DataFrame()

        # Rename columns to match what our chart expects: 'open', 'high', 'low', 'close'
        df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        
        print(f"Successfully fetched {len(df)} data points for {ticker}.")
        return df

    except Exception as e:
        import traceback
        print(f"An error occurred while fetching yfinance data for {ticker}:")
        traceback.print_exc()
        return pd.DataFrame()