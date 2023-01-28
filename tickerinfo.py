import yfinance as yf
from flask import Flask, request, Blueprint
import pyrebase
import json
tickerinfo = Blueprint('tickerinfo', __name__)

#/api/tickerinfo?tickerArr=AAPL&tickerArr=GOOG

@tickerinfo.route(f"/api/tickerinfo", methods=["GET"])
def get_price():
    ticker_arr = request.args.getlist("tickerArr")
    if not ticker_arr:
        return "No tickerArr parameter in the request", 400
    info_dict = {}
    for ticker in ticker_arr:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        info_dict[ticker] = price
    return info_dict
  
