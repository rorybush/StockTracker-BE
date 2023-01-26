from flask import Flask, request, Blueprint
import pyrebase

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
    portfolioList = []
    results = db.child('users-db').child(uid).get()
    for result in results.each():
        portfolioList.append({result.key(): result.val()})
    return portfolioList

@portfolio.route(f"/api/portfolio/<uid>/add", methods=["POST", 'GET'])
def addPortfolio(uid):
    stock = request.form.get('stock')
    date = request.form.get('date')
    quantity = request.form.get('quantity')
    db.child('users-db').child(uid).child('appl').set({
    'name': 'aapl',
    'date': 2342343,
    'quantity': 23,
    'price': 4
    })

@portfolio.route(f"/api/portfolio/<uid>/update", methods=["PATCH", 'GET'])
def updatePortfolio(uid):
    stock = request.form.get('stock')
    date = request.form.get('date')
    quantity = request.form.get('quantity')
    db.child('users-db').child(uid).child(stock).update({
    'date': date,
    'quantity': quantity,
})

@portfolio.route(f"/api/portfolio/<uid>/remove", methods=["DELETE", 'GET'])
def removeStockFromPortfolio(uid):
    stock = request.form.get('stock')
    db.child('users-db').child(uid).child(stock).remove()

@portfolio.route(f"/api/portfolio/<uid>/wipe", methods=["DELETE", 'GET'])
def removePortfolio(uid):
    db.child('users-db').child(uid).remove()

