import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, Blueprint
from sklearn.metrics import precision_score

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

@stockai.route('/api/stockai/<stockname>')
def stock_ai(stockname):
    stock = yf.Ticker(stockname)
    sh = stock.history(period='max')
    del sh['Dividends']
    del sh['Stock Splits']
    sh['Tomorrow'] = sh['Close'].shift(-1)
    sh['Target'] = (sh['Tomorrow'] > sh['Close']).astype(int)
    sh = sh.loc['1995-01-01':].copy()
    time_horizons = [1, 2, 5, 30, 63, 126, 252, 378, 504, 1008]
    stock_predictors = []
    for horizon in time_horizons:
        rolling_averages = sh.rolling(horizon).mean()

        ratio_column = f"Close_Ratio_{horizon}"
        sh[ratio_column] = sh['Close'] / rolling_averages['Close']

        trend_column = f'Trend_{horizon}'
        sh[trend_column] = sh.shift(1).rolling(horizon).sum()['Target']

        stock_predictors += [ratio_column, trend_column]
    sh = sh.dropna()
    model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
    stockPredictions = backtest(sh, model, stock_predictors)
    modelPredictions = stockPredictions['Predictions'] == 1
    daysWhereModelPredicts = stockPredictions[modelPredictions]
    daysWhereModelPredicts = daysWhereModelPredicts.drop(columns=['Target'])
    print(daysWhereModelPredicts)
    jsonModel = daysWhereModelPredicts.to_json()
    return jsonModel
