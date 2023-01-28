import yfinance as yf
from flask import Flask, request, Blueprint
import pyrebase
import json
tickerinfo = Blueprint('tickerinfo', __name__)


@tickerinfo.route(f"/api/tickerinfo", methods=["GET"])
def get_price():
    ticker_string = request.args.getlist("tickerArr")
    if not ticker_string:
        return "No tickerArr parameter in the request", 400
    ticker_arr = ticker_string.split(',')
    info_arr = []
    for ticker in ticker_arr:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        info_arr.append({ticker: price})
    return info_arr
  
