# app/services/stock_service.py
import os
import requests

ALPHA_VANTAGE_API_KEY = os.getenv("STOCK_API_KEY")  # Ensure this is set in your .env
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def get_realtime_price(ticker: str) -> float:
    """
    Fetches the real-time stock price for the given ticker symbol using Alpha Vantage.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
    data = response.json()

    # Navigate the JSON response to extract price
    try:
        price = float(data["Global Quote"]["05. price"])
        return price
    except (KeyError, ValueError):
        raise Exception(f"Could not retrieve price for ticker: {ticker}")
