from pytickersymbols import PyTickerSymbols
from flask import Flask, Blueprint

stockList = Blueprint('stockList', __name__)

stock_data = PyTickerSymbols()
ftse = stock_data.get_stocks_by_index('FTSE 100')
sp500 = stock_data.get_stocks_by_index('S&P 500')
sp100 = stock_data.get_stocks_by_index('S&P 100')
nasdaq100 = stock_data.get_stocks_by_index('NASDAQ 100')
dow = stock_data.get_stocks_by_index('DOW JONES')
cac40 = stock_data.get_stocks_by_index('CAC 40')

allStocks = []
allStocks.extend(ftse)
allStocks.extend(sp500)
allStocks.extend(sp100)
allStocks.extend(nasdaq100)
allStocks.extend(dow)
allStocks.extend(cac40)

@stockList.route(f'api/stocklist', methods=["GET"])
def stockListByExchange():
    filteredData = []
    for stock in list(allStocks):
        filteredStock = {
        'companyName': stock['name'],
        'symbol': stock['symbol']
        }
        filteredData.append(filteredStock)
    return filteredData

@stockList.route(f'api/stocklist/ftse', methods=["GET"])
def ftseStockList():
    ftse = stock_data.get_stocks_by_index('FTSE 100')
    filteredData = []
    for stock in list(ftse):
        filteredStock = {
        'companyName': stock['name'],
        'symbol': stock['symbol']
        }
        filteredData.append(filteredStock)
    return filteredData

@stockList.route(f'api/stocklist/nasdaq', methods=["GET"])
def nasdaqStockList():
    nasdaq100 = stock_data.get_stocks_by_index('NASDAQ 100')
    filteredData = []
    for stock in list(nasdaq100):
        filteredStock = {
        'companyName': stock['name'],
        'symbol': stock['symbol']
        }
        filteredData.append(filteredStock)
    return filteredData

@stockList.route(f'api/stocklist/sp100', methods=["GET"])
def spStockList():
    sp100 = stock_data.get_stocks_by_index('S&P 100')
    filteredData = []
    for stock in list(sp100):
        filteredStock = {
        'companyName': stock['name'],
        'symbol': stock['symbol']
        }
        filteredData.append(filteredStock)
    return filteredData