# core/ingest.py
import os
import pandas as pd
from dotenv import load_dotenv
from newsapi import NewsApiClient
from gnews import GNews
import finnhub
from datetime import date, timedelta
from core.nlp import get_sentiment_score
from core.mapping import map_headline_to_assets

load_dotenv()

def fetch_newsapi_articles(query):
    """Fetches news from NewsAPI."""
    print(f"Fetching NewsAPI for: {query}")
    client = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    response = client.get_everything(q=query, language='en', sort_by='relevancy')
    return _normalize_articles(response.get('articles', []), 'NewsAPI')

def fetch_gnews_articles(query):
    """Fetches news from GNews."""
    print(f"Fetching GNews for: {query}")
    client = GNews(language='en', country='IN', period='7d')
    response = client.get_news(query)
    return _normalize_articles(response, 'GNews')

def fetch_finnhub_news(query):
    """Fetches news from Finnhub."""
    print(f"Fetching Finnhub for: {query}")
    client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    response = client.company_news(query, _from=one_week_ago.strftime("%Y-%m-%d"), to=today.strftime("%Y-%m-%d"))
    return _normalize_articles(response, 'Finnhub')

def _normalize_articles(articles, source_name):
    """Unifies article data from different sources into a standard format."""
    normalized = []
    for article in articles:
        title = article.get('title') or article.get('headline', '')
        if not title or title == '[Removed]':
            continue

    
        published_at = article.get('publishedAt') or article.get('published date')
        if 'datetime' in article:
            published_at = pd.to_datetime(article['datetime'], unit='s')
        
        url = article.get('url') or article.get('link')

        normalized.append({
            'published': pd.to_datetime(published_at, errors='coerce', utc=True),
            'title': title,
            'summary': article.get('summary') or article.get('description', ''),
            'source': source_name,
            'sentiment': get_sentiment_score(title),
            'assets': map_headline_to_assets(title)
        })
        
    if not normalized:
        return pd.DataFrame()
        
    df = pd.DataFrame(normalized).dropna(subset=['published'])
    return df.explode('assets')