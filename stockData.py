import yfinance as yf
from flask import Flask, request, Blueprint
import pyrebase
import json

firebaseConfig = {
    "apiKey": "AIzaSyABF_dh8WSnwqCmlX01PiQ7hiOFhleX4Bc",
    "authDomain": "southcoders-be.firebaseapp.com",
    "projectId": "southcoders-be",
    "databaseURL": "https://southcoders-be-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "southcoders-be.appspot.com",
    "messagingSenderId": "851060036490",
    "appId": "1:851060036490:web:4b2a072e7b5fd2d504ee73",
    "measurementId": "G-7R5FPYEH2F"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

stockData = Blueprint('stockData', __name__)

# stock = yf.Ticker("AAPL")
# stockinfo=stock.info
# for key,value in stockinfo.items():
#     print(key, ':', value)


@stockData.route(f"/api/stockdata/<symbol>", methods=["GET"])
def getStockData(symbol):
    stock = yf.Ticker(symbol)
    stockBasicInfo = stock.basic_info
    stockInfo =  {
        'tickerSymbol': symbol,
       'marketCap': stockBasicInfo['market_cap'],
       'lastPrice': stockBasicInfo['last_price'],
       'previousClose': stockBasicInfo['previous_close'],
       'open': stockBasicInfo['open'],
       'dayHigh': stockBasicInfo['day_high'],
       'dayLow': stockBasicInfo['day_low'],
       'lastVolume': stockBasicInfo['last_volume'].astype(float),
        'yearHigh': stockBasicInfo['year_high'],
        'yearLow': stockBasicInfo['year_low'],
        'employees': stockBasicInfo['fullTimeEmployees'],
        'website': stockBasicInfo['website'],
        'headquarter': stockBasicInfo['country'],
        'pricetobook': stockBasicInfo['priceToBook'],
        'bookValue': stockBasicInfo['bookValue'],
        'ask': stockBasicInfo['ask'],
        'logo': stockBasicInfo['logo_url'],
        'summary': stockBasicInfo['longBusinessSummary'],

 }
    return stockInfo

