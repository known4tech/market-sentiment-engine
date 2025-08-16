# scripts/load_data.py
import pandas as pd
import os

def load_csv(ticker):
    """
    Loads CSV for a given ticker and returns a clean DataFrame.
    Handles extra headers or formatting issues automatically.
    """
    path = f"data/{ticker.lower()}.csv"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist. Run download_tickers.py first.")
    
    # Read CSV and automatically detect first valid header row
    df = pd.read_csv(path, index_col=0, parse_dates=True, skip_blank_lines=True)
    
    # Sometimes CSV has extra header rows, filter out non-numeric rows
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna(how='all')  # Drop rows where all columns are NaN

    # Ensure 'Date' is index
    if df.index.name != 'Date':
        df.index.name = 'Date'
    
    return df