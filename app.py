from flask import Flask
from flask_cors import CORS
from portfolio import portfolio
from chartData import chartData
from stocknews import stocknews
from stockData import stockData
from stockList import stockList
from tickerinfo import tickerinfo
from events import calendar
from stockai import stockai

app = Flask(__name__)
CORS(app)
app.register_blueprint(portfolio, url_prefix="")
app.register_blueprint(chartData, url_prefix="")
app.register_blueprint(stocknews, url_prefix="")
app.register_blueprint(stockData, url_prefix="")
app.register_blueprint(stockList, url_prefix="")
app.register_blueprint(tickerinfo, url_prefix="")
app.register_blueprint(calendar, url_prefix="")
app.register_blueprint(stockai, url_prefix="")



if __name__ == "__main__":
    app.run(debug=True)