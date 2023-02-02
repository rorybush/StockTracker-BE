from flask import Flask, request, Blueprint, jsonify
import pyrebase
import yfinance as yf


portfolio = Blueprint('portfolio', __name__)

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


@portfolio.route(f"/api/portfolio/<uid>", methods=["GET"])
def getPortfolio(uid):
    try:
        portfolioList = []
        results = db.child('users-portfolio').child(uid).get()
        for result in results.each():
            portfolioList.append({result.key(): result.val()})
        print(portfolioList)
        return portfolioList
    except:
        return jsonify(message='No Stocks in Portfolio'),500


@portfolio.route(f"/api/portfolio/<uid>/add", methods=["POST"])
def addPortfolio(uid):
    newStockData = request.json
    dataToSend = {
    'name': newStockData['name'],
    'date': newStockData['date'],
    'quantity': newStockData['quantity'],
    'price': newStockData['price']
    }
    db.child('users-portfolio').child(uid).child(newStockData['name']).set(dataToSend)
    return dataToSend


@portfolio.route(f"/api/portfolio/<uid>/update", methods=["PATCH"])
def updatePortfolio(uid):
    newStockData = request.json
    dataToPatch = {
    'name': newStockData['name'],
    'date': newStockData['date'],
    'quantity': newStockData['quantity'],
    'price': newStockData['price']
    }
    db.child('users-portfolio').child(uid).child(newStockData['name']).update(dataToPatch)
    return dataToPatch

@portfolio.route(f"/api/portfolio/<uid>/removestock", methods=["DELETE"])
def removeStockFromPortfolio(uid):
    stockToRemove = request.json
    db.child('users-portfolio').child(uid).child(stockToRemove['stock']).remove()
    return 'Stock Deleted'

@portfolio.route(f"/api/portfolio/<uid>/deleteportfolio", methods=["DELETE"])
def removePortfolio(uid):
    db.child('users-portfolio').child(uid).remove()
    return 'Portfolio Deleted'

@portfolio.route(f"/api/portfolio/<uid>/pl", methods=["GET"])
def getPortfolioProfitLoss(uid):
    try:
        userPortfolio = getPortfolio(uid)
        portfolioPL = []
        for stock in userPortfolio:
            for key, value in stock.items():
                stock = yf.Ticker(value['name']).fast_info
                todaysPrice = stock['last_price']
                portfolioPL.append({
                    'name': value['name'],
                    'dateBought': value['date'],
                    'quantity': int(value['quantity']),
                    'buyPrice': int(value['price']),
                    'totalBuyPrice': int(value['quantity']) * int(value['price']),
                    'todaysPrice': int(todaysPrice),
                    'todaysTotalPrice': todaysPrice * int(value['quantity']),
                    'ProfitLoss': todaysPrice * int(value['quantity']) - int(value['quantity']) * int(value['price'])
                })
        return portfolioPL
    except:
        return jsonify(message='Not enough data to display Profit/Loss'),500