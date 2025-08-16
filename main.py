# app/main.py (FINAL VERSION)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ingest import fetch_newsapi_articles, fetch_gnews_articles, fetch_finnhub_news
from core.market import fetch_price_data
from core.sentiment import calculate_asset_specific_sentiment
from core.stats import generate_signals

st.set_page_config(page_title="AMSE v2.1", page_icon="📈", layout="wide")

NEWS_SOURCES = {"NewsAPI": fetch_newsapi_articles, "GNews": fetch_gnews_articles, "Finnhub": fetch_finnhub_news}
ASSET_MAP = {
    "NIFTY 50 (India)": "^NSEI", "SENSEX (India)": "^BSESN", "USD/INR": "INR=X",
    "S&P 500 (US)": "^GSPC", "Nikkei 225 (Japan)": "^N225", "Gold": "GC=F",
    "Brent Crude Oil": "BZ=F", "Reliance (India)": "RELIANCE.NS", "Apple (US)": "AAPL"
}

# --- CACHING FIX ---
# The cached function now accepts the SOURCE NAME (a string) instead of the function object.
@st.cache_data(ttl=900)
def get_news_data(source_name, query):
    # It looks up the correct function inside the cached function.
    source_func = NEWS_SOURCES[source_name]
    print(f"Fetching news from source: {source_func.__name__}")
    return source_func(query)

@st.cache_data(ttl=900)
def get_price_data(ticker):
    return fetch_price_data(ticker)

# --- SIDEBAR ---
st.sidebar.title("Controls")
selected_asset = st.sidebar.selectbox("Select Asset", list(ASSET_MAP.keys()))
selected_ticker = ASSET_MAP[selected_asset]
selected_news_source_name = st.sidebar.selectbox("Select News Source", list(NEWS_SOURCES.keys()))

# --- DATA LOADING ---
price_df = get_price_data(selected_ticker)
# --- CACHING FIX ---
# Pass the SELECTED NAME (string) to the cached function.
news_df = get_news_data(selected_news_source_name, selected_asset)
sentiment_by_asset = calculate_asset_specific_sentiment(news_df)
asset_specific_sentiment = sentiment_by_asset.get(selected_asset)
analysis = generate_signals(price_df, asset_specific_sentiment if asset_specific_sentiment is not None else pd.Series())

# --- HEADER ---
st.title("📈 ASSE: Asset-Specific Sentiment Engine")
st.caption(f"Displaying analysis for **{selected_asset}** using news from **{selected_news_source_name}**.")

# --- RECOMMENDATION BOX ---
if analysis:
    cols = st.columns(4)
    cols[0].metric(f"Price ({selected_ticker})", analysis['latest_price'], analysis['price_change'])
    cols[1].metric("Asset-Specific Sentiment", analysis['latest_sentiment'])
    cols[2].metric("Sentiment Z-Score", analysis['sentiment_z_score'], help="How unusual is current sentiment? (>1.5 is significant)")
    cols[3].metric("Signal", analysis['signal'])
    st.info(f"**Recommendation:** {analysis['recommendation']}")
else:
    st.warning("Not enough data to generate a recommendation.")

st.divider()

# --- CHART ---
st.subheader("Price vs. Asset-Specific Sentiment")
if not price_df.empty:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=price_df.index, open=price_df['open'], high=price_df['high'],
                                 low=price_df['low'], close=price_df['close'], name='Price'), secondary_y=False)
    if asset_specific_sentiment is not None and not asset_specific_sentiment.empty:
        fig.add_trace(go.Scatter(x=asset_specific_sentiment.index, y=asset_specific_sentiment.values,
                                 name='Sentiment', line=dict(color='yellow', width=2)), secondary_y=True)

    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)
    fig.update_yaxes(title_text="Price", secondary_y=False, autorange=True)
    fig.update_yaxes(title_text="Sentiment", secondary_y=True, range=[-1, 1])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Could not fetch price data.")

# --- NEWS TABLE ---
st.subheader(f"Relevant News from {selected_news_source_name}")
if not news_df.empty:
    relevant_news = news_df[news_df['assets'] == selected_asset]
    st.dataframe(relevant_news[['published', 'sentiment', 'title', 'source']], height=400, hide_index=True)
else:
    st.error("Could not fetch articles.")