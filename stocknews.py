import yfinance as yf
import finnhub
from newsapi import NewsApiClient
import json


from datetime import date, timedelta

newsapi = NewsApiClient(api_key='7a9d47e5bf3844999c8f189d2b8f9637')
finnhub_client = finnhub.Client(api_key="cf80idiad3i8qmbtgqmgcf80idiad3i8qmbtgqn0")

today = date.today()
month_ago = today - timedelta(days=30)

def get_newsapi_company_news(ticker, limit=15):
    try:
        sources = "the-wall-street-journal, cnbc, bloomberg, reuters, bbc-news"
        
        company_news = newsapi.get_everything(q=ticker, sources=sources,  language='en', sort_by="relevancy", page=1)
        if(len(company_news) <= 1):
            
             return 'No articles found'
        else:
             return company_news['articles'][:limit]
    except: 
        return 'Error getting articles from the news api'

def get_company_news_yfinance(ticker):
    stock = yf.Ticker(ticker)
    return stock.news

print(get_company_news_yfinance('HCC'))



def get_company_news(ticker, limit=15):
    try: 
        stock_news = finnhub_client.company_news(ticker, _from=month_ago.isoformat(), to=today.isoformat())
        
        if not stock_news :
             news = get_newsapi_company_news(ticker)
             news = [{'label': f'News {i+1}', **item} for i, item in enumerate(news)]
             return  news[:limit]
        else:
            stock_news = [{'label': f'Stock News {i+1}', **item} for i, item in enumerate(stock_news)]
            return stock_news
    
    except:
        return 'Errors getting company news from api'




#portfolio news without newsapi limit of articles per stock
def get_portfolio_news(*args, limit=5):
    news_arr = []
    for stock in args:
        stock_news = get_company_news(stock)
        news_arr.append(stock_news[:limit])
    return news_arr 
        


# print(get_portfolio_news("Aviva", "AAPL", "MSFT", "GOOGL", "WME"))