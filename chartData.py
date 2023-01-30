import yfinance as yf
from flask import Flask, Blueprint
import json
import pandas as pd

chartData = Blueprint('stock', __name__)


@chartData.route('/stock/<stockname>')
def chart_data(stockname):
    stock = yf.Ticker(stockname)
    stockHistory = stock.history(period="max")
    stockHistory = stockHistory.reset_index()
    del stockHistory['Dividends']
    del stockHistory['Stock Splits']
    stockHistory['Date'] = pd.to_datetime(stockHistory["Date"].dt.strftime('%Y-%m-%d'))
    stockJson = stockHistory.to_json(date_format='iso')
    return {'stock': stockJson}
