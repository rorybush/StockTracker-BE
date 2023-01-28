import yfinance as yf
from flask import Flask, request, Blueprint
import pyrebase
import json
tickerinfo = Blueprint('tickerinfo', __name__)


@tickerInfo.route(f"/api/tickerinfo", methods=["GET"])
def get_price():
    ticker_arr = request.args.getlist("tickerArr")
    if not ticker_arr:
        return "No tickerArr parameter in the request", 400
    info_arr = []
    for ticker in ticker_arr:
        stock = yf.Ticker(ticker)
        price = stock.latestPrice 
        info_arr.append({ticker: price})
    return info_arr
  

