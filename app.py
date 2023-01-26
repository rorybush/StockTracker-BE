from flask import Flask
from flask_cors import CORS
from authentication import authentication
from portfolio import portfolio
from chartData import chartData


app = Flask(__name__)
CORS(app)
app.register_blueprint(portfolio, url_prefix="")
app.register_blueprint(authentication, url_prefix="")
app.register_blueprint(chartData, url_prefix="")


app.secret_key = "secret"


if __name__ == "__main__":
    app.run(port=1111)
