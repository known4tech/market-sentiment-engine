# core/mapping.py

# This maps keywords to the asset names used in your app's dropdown
ASSET_KEYWORDS = {
    "NIFTY 50 (India)": ["nifty", "nsei", "indian market"],
    "SENSEX (India)": ["sensex", "bsesn"],
    "USD/INR": ["rupee", "inr", "rbi"],
    "S&P 500 (US)": ["s&p", "spx", "us market", "fed", "powell"],
    "Nikkei 225 (Japan)": ["nikkei", "n225", "bank of japan", "boj"],
    "Gold": ["gold", "bullion", "xau"],
    "Brent Crude Oil": ["oil", "crude", "brent", "opec"],
    "Reliance (India)": ["reliance", "ril"],
    "Apple (US)": ["apple", "aapl", "iphone"]
}

def map_headline_to_assets(headline):
    """ Scans a headline for keywords and tags it with relevant assets. """
    mapped_assets = set()
    headline_lower = headline.lower()
    for asset, keywords in ASSET_KEYWORDS.items():
        if any(keyword in headline_lower for keyword in keywords):
            mapped_assets.add(asset)
    return list(mapped_assets) if mapped_assets else ["General"]