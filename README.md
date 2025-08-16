# AMSE: Asset-Specific Sentiment Engine 📈

**Live Demo:** **[🚀 View the Live Application Here]([https://your-app-url.streamlit.app/](https://market-sentiment-engine.streamlit.app/))**

## 🎯 Project Goal

The Asset-Specific Sentiment Engine (AMSE) is a comprehensive dashboard designed to ingest live financial news, perform sentiment analysis, and correlate it with market price data to generate actionable insights. The goal is to provide a clear, data-driven narrative of market conditions for various assets, including Indian and global indices, forex, and commodities.

This project was built from the ground up to be a zero-cost, high-impact tool that showcases modern data science and application development practices.

---

## ✨ Key Features

* **Multi-Source News Ingestion:** Aggregates news from various global sources using the NewsAPI.
* **Historical Price Data:** Fetches and displays daily OHLC price data from Yahoo Finance.
* **Asset-Specific Sentiment Analysis:**
    * Uses a VADER sentiment model to score headline sentiment.
    * Employs a keyword-based mapping system (`core/mapping.py`) to tag each news article with the specific financial asset(s) it impacts.
    * Calculates a rolling 7-day average sentiment score *per asset* for a smoother, more reliable signal.
* **Automated Market Narrative:** Generates a plain-English summary and a clear trading signal (e.g., "Strong Buy 🟢") based on the statistical significance (Z-score) of the current sentiment.
* **Interactive Dashboard:** A fully interactive web application built with Streamlit and Plotly, featuring:
    * A professional summary dashboard with key metrics.
    * An interactive candlestick chart with a sentiment overlay.
    * A filterable table of the latest relevant news headlines.
* **Mobile-Friendly Design:** The layout is responsive and provides a clean user experience on both desktop and mobile devices.

---

## 🛠️ Technology Stack

* **Backend:** Python
* **Data Analysis & Manipulation:** Pandas, NumPy
* **Web Framework & UI:** Streamlit
* **Data Visualization:** Plotly
* **Data Sources:** yfinance (for price data), NewsAPI (for news data)
* **NLP/Sentiment Analysis:** NLTK (VADER)
* **Deployment:** Streamlit Community Cloud

---

## 🏗️ How to Run Locally

To run this application on your own machine, please follow these steps:

**1. Clone the Repository**
```bash
git clone [https://github.com/known4tech/market-sentiment-engine](https://github.com/known4tech/market-sentiment-engine)
cd your-repo-name
