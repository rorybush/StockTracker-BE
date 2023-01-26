from flask import Flask
from flask_cors import CORS
from portfolio import portfolio
from chartData import chartData
from stocknews import stocknews

app = Flask(__name__)
CORS(app)
app.register_blueprint(portfolio, url_prefix="")
app.register_blueprint(chartData, url_prefix="")
app.register_blueprint(stocknews, url_prefix="")



# app.secret_key = "secret"


if __name__ == "__main__":
    app.run()

# port=1111