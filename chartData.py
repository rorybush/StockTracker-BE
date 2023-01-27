import yfinance as yf
from flask import Flask, Blueprint
import json
import pandas as pd

chartData = Blueprint('stock', __name__)


stock = yf.Ticker('tsla')
stockHistory = stock.history(period="max")
stockHistory = stockHistory.reset_index()
del stockHistory['Dividends']
del stockHistory['Stock Splits']

stockHistory['Date'] = pd.to_datetime(stockHistory["Date"].dt.strftime('%Y-%m-%d'))


stockJson = stockHistory.to_json(date_format='iso')


@chartData.route('/stock')
def chart_data():
    return {'stock': stockJson}
