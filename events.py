
from flask import Flask, request, Blueprint
import pyrebase
import csv
import requests

calendar = Blueprint('calendar', __name__)

@calendar.route(f"/api/calendar/<ticker>", methods=["GET"])
def get_stock_events(ticker):
    CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={ticker}&horizon=3month&apikey=X0BKH2D8ZU87LBZP'

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        calendar = list(cr)
        return calendar
        


