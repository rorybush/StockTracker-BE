import yfinance as yf
from flask import Flask, request, Blueprint
import pyrebase
import json
tickerinfo = Blueprint('tickerinfo', __name__)


@tickerinfo.route(f"/api/tickerinfo", methods=["GET"])
def get_price():
    ticker_arr = request.args.get("tickerArr")
    if not ticker_arr:
        return "No tickerArr parameter in the request", 400
        ticker_arr = ticker_str.split(',')
    info_arr = []
    for ticker in ticker_arr:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        info_arr.append({ticker: price})
    return info_arr
  
