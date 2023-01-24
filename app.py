from flask import Flask, session, render_template, request, redirect
import pyrebase
from authentication import auth, firebaseConfig

app = Flask(__name__)

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
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
