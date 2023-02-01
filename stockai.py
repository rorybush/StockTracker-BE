import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, Blueprint
from sklearn.metrics import precision_score
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime



stockai = Blueprint('stockai', __name__)

def predict(train, test, predictors, model):
    model.fit(train[predictors], train['Target'])
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds >= 0.55] = 1
    preds[preds < 0.55] = 0
    preds = pd.Series(preds, index=test.index, name='Predictions')
    combined = pd.concat([test['Target'], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2016, step=252):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        trainData = data.iloc[0:i].copy()
        testData = data.iloc[i: i+step].copy()
        predictions = predict(trainData, testData, predictors, model)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)



# stockPredictions['Date'] = pd.to_datetime(stockPredictions["Date"].dt.strftime('%Y-%m-%d'))



# model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
# stockPredictions = backtest(sh, model, stock_predictors)
# modelPredictions = stockPredictions['Predictions'] == 1
# daysWhereModelPredicts = stockPredictions[modelPredictions]
# daysWhereModelPredicts = daysWhereModelPredicts.tail(10)

@stockai.route('/api/stockai/<stockname>')
def stock_ai(stockname):
    stock = yf.Ticker(stockname)
    model = LinearRegression(n_jobs=-1)
    sh = stock.history(period='max')
    del sh['Dividends']
    del sh['Stock Splits']
    sh['Tomorrow'] = sh['Close'].shift(-1)
    sh['Target'] = (sh['Tomorrow'] > sh['Close']).astype(int)
    sh = sh.loc['2000-01-01':].copy()
    time_horizons = [2, 5, 10, 21, 252, 378, 504, 1008]
    stock_predictors = []
    for horizon in time_horizons:
        rolling_averages = sh.rolling(horizon).mean()

        ratio_column = f"Close_Ratio_{horizon}"
        sh[ratio_column] = sh['Close'] / rolling_averages['Close']

        trend_column = f'Trend_{horizon}'
        sh[trend_column] = sh.shift(1).rolling(horizon).sum()['Target']

        stock_predictors += [ratio_column, trend_column]
    sh = sh.dropna()
    forecastOnePercent = int(math.ceil(0.01 * len(sh)))
    sh['label'] = sh['Tomorrow'].shift(-forecastOnePercent)
    X = np.array(sh.drop(['Tomorrow'], 1))
    X = preprocessing.scale(X)
    X_lately = X[-forecastOnePercent:]
    X = X[:-forecastOnePercent]
    X_lately = X[-forecastOnePercent:]
    y = np.array(sh['label'])
    y = y[:-forecastOnePercent]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model.fit(X_train, y_train)
    forecast_set = model.predict(X_lately)
    sh['Forecast'] = np.nan
    last_date = sh.iloc[-1].name
    last_unix = last_date
    next_unix = last_unix + datetime.timedelta(days=1)
    for i in forecast_set:
        next_date = next_unix
        next_unix += datetime.timedelta(days=1)
        sh.loc[next_date] = [np.nan for _ in range(len(sh.columns)-1)]+[i]
    sh = sh.reset_index()
    stockPredictions = sh[['Date','Forecast']]
    today = datetime.datetime.today().date()
    stockPredictions['Date'] = stockPredictions['Date'].dt.date
    stockPredictions5Days = stockPredictions[(stockPredictions['Date'] > today) & (stockPredictions['Date'] <= today + pd.Timedelta(days=5))]
    jsonModel = stockPredictions5Days.to_json()
    return jsonModel