from newsapi import NewsApiClient
import http.client, urllib.parse



newsapi = NewsApiClient(api_key='7a9d47e5bf3844999c8f189d2b8f9637')

def get_finance_news(limit=15):
    try:
        sources = "the-wall-street-journal, cnbc, bloomberg, reuters, financial-times"
        
        finance_articles = newsapi.get_everything(q='business', sources=sources,  language='en', sort_by="relevancy", page=1)
    
        if(len(finance_articles) <= 1):
             return 'No articles found'
        else:
             print(finance_articles[0])
             return finance_articles['articles'][:limit]
    except: 
        return 'Error getting articles from the api'
     

  
    
    

def get_company_news(ticker, limit=10):
    try:
        sources = "the-wall-street-journal, cnbc, bloomberg, reuters, financial-times"
        
        company_news = newsapi.get_everything(q=ticker, sources=sources,  language='en', sort_by="relevancy", page=1)
        if(len(company_news) <= 3):
             return 'No articles found'
        else:
             return company_news['articles'][:limit]
    except: 
        return 'Error getting articles from the api'
     




print(get_finance_news())
# print(get_company_news('HCC'))

# mediastack 

#  mediastack api key:
#   becf95e96f5c4cfbcc658f06ba530d0b

# def finance_news():
#     conn = http.client.HTTPConnection('api.mediastack.com')

#     params = urllib.parse.urlencode({
#         'access_key': 'becf95e96f5c4cfbcc658f06ba530d0b',
#         'category': 'finance',
#         'language': 'en',
#         'sort_by': 'popularity',
#         'sources': 'financial+times'
#         })

#     conn.request('GET', '/v1/news?{}'.format(params))

#     res = conn.getresponse()
#     data=res.read()

#     return data.decode('utf-8')




# print(finance_news())

