from flask import Flask, session, render_template, request, redirect
import pyrebase
from authentication import auth

app = Flask(__name__)

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
database = firebase.database()

data = {
    "id": 283,
    "username": "test",
    "age": 24,
    "location": "london"
}

database.child("users-db").child(data["id"]).set(data)


auth = firebase.auth()

app.secret_key = "secret"


@app.route("/", methods=["POST", "GET"])
def index():
    if ("user" in session):
        return render_template("./loggedin.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        database.child("users-db").child("test").set({"email": email})
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
        except:
            return "failed to login"
    return render_template("./index.html")


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")


@app.route("/sign-up", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = auth.create_user_with_email_and_password(email, password)
        username = request.form.get("username")
        userID = user["localId"]
        data = {
            "email": email,
            "username": username,
        }
        database.child("users-db").child(userID).set(data)
        return render_template("./index.html")

    return render_template("./sign-up.html")


if __name__ == "__main__":
    app.run(port=1111)
