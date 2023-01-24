from flask import Flask, session, render_template, request, redirect
import pyrebase
from authentication import auth

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

# user = auth.create_user_with_email_and_password(email, password)
# userID = user["localId"]

def addPortfolio(uid, stockname, date, quantity):
    db.child('users-db').child(uid).child(stockname).set({
    'date': date,
    'quantity': quantity,
})

def updatePortfolio(uid, stockname, date, quantity):
    db.child('users-db').child(uid).child(stockname).update({
    'date': date,
    'quantity': quantity,
})

def removePortfolio(uid):
    db.child('users-db').child(uid).remove()

def removeStockFromPortfolio(uid, stockname):
    db.child('users-db').child(uid).child(stockname).remove()

def getPortfolio(uid):
    portfolioList = []
    results = db.child('users-db').child(uid).get()
    for result in results.each():
        portfolioList.append({result.key(): result.val()})
    return portfolioList


# results = db.child('q5B0Tm2BoQekynXWR7q6WtlikfI2').get()

# for result in results.each():
#     print({result.key(): result.val()})
    
# db.child('users-db').child('q5B0Tm2BoQekynXWR7q6WtlikfI2').child('aapl').set({
#     'portfoloId': 1
#     'date': 3453534,
#     'quantity': 100,
# })


