import yfinance as yf
from datetime import datetime, timedelta

today = datetime.now()
month_ago = today - timedelta(days=30)


def get_general_finance_news(limit=5):
    try:
        news = yf.Ticker('N/A').news
        return news[:limit]
    except: 
        return 'Error getting general finance news from api'

# print(get_general_finance_news(2))

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

def get_markets_news(ticker, limit=15):
    try: 
        market = yf.Ticker(f"^{ticker}")
        market_news = market.news
        if not market_news :
             return  'No Articles Found'
        else:
            return market_news[:limit]
    
    except:
        return 'Error getting company news from api'

# print(get_markets_news('FTSE', 2))


def get_portfolio_news(tickerArr, limit=5):
    news_arr = []
    for stock in tickerArr:
        stock_news = get_company_news(stock)
        news_arr.append(stock_news[:limit])
    return news_arr 
        


# print(get_portfolio_news(["Aviva", "AAPL", "MSFT", "GOOGL", "WME"]))