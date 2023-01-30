from flask import Flask, request, Blueprint
import pyrebase
import yfinance as yf
from datetime import datetime, timedelta

stocknews = Blueprint('stocknews', __name__)

today = datetime.now()
month_ago = today - timedelta(days=30)


@stocknews.route("/api/news", methods=["GET"])
def get_general_finance_news(limit=10):
    try:
        news = yf.Ticker('N/A').news
        return news[:limit]
    except: 
        return 'Error getting general finance news from api'

# print(get_general_finance_news(2))

@stocknews.route(f"/api/news/<ticker>", methods=["GET"])
def get_company_news(ticker, limit=15):
    try: 
        stock = yf.Ticker(ticker)
        stock_news = stock.news
        if not stock_news :
             return  'No Articles Found'
        else:
            return stock_news[:limit]
    
    except:
        return 'Error getting company news from api'

# print(get_company_news('Aviva', 1))

@stocknews.route(f"/api/news/markets/<symbol>", methods=["GET"])
def get_markets_news(symbol, limit=15):
    try: 
        market = yf.Ticker(f"^{symbol}")
        market_news = market.news
        if not market_news :
             return  'No Articles Found'
        else:
            return market_news[:limit]
    
    except:
        return 'Error getting company news from api'

# print(get_markets_news('FTSE', 2))

@stocknews.route("/api/news/portfolio", methods=["GET"])
def get_portfolio_news():
    ticker_arr = request.args.getlist("tickerArr")
    limit = request.args.get("limit", 5)
    if not ticker_arr:
        return "No tickerArr parameter in the request", 400
    news_arr = []
    for stock in ticker_arr:
        stock_news = get_company_news(stock)
        news_arr.append(stock_news[:limit])
    return news_arr
  


# print(get_portfolio_news(["Aviva", "AAPL", "MSFT", "GOOGL", "WME"]))