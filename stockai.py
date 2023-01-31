import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

#yfinance gets the data
#pandas manipulates the data
#scikit is sued to train and evaluate the RandomForestClassifier which is a type of machine learning model

stock = yf.Ticker('msft')

sh = stock.history(period='max')

del sh['Dividends']
del sh['Stock Splits']

sh['Tomorrow'] = sh['Close'].shift(-1)

sh['Target'] = (sh['Tomorrow'] > sh['Close']).astype(int)

sh = sh.loc['1990-01-01':].copy()

#data up to the last 100 days, this is used to train the model
train = sh.iloc[:-100]
#data for the last 100 days, this is used to test the model
test = sh.iloc[-100:]

#Close, Volume, Open, High, Low data are all used to predict
predictors = ['Close', 'Volume', 'Open', 'High', 'Low']


#this runs the test data multiple times, using different time intervals returning an aggregate of the results
#it takes in the msft data, machine learning model, the predictors, the start value and step.
#the start value chooses at what point you start to train your data, there are around 250 trading days a year so this uses 10 years of data to train the model
#the step is 250 so we train the model for a year, then we go into the next year.
#we take the first 10 years of data to predict the 11th year, then we take the 11 years of data to predict the 12th year etc.
def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i: i+step].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)

#this is the time horizon, 2 is for every 2 days, 5 for every 5 days etc.
horizons = [2,5,60,250,1000]
new_predictors = []

#we create a a column for each time horizon, this calcultes the trend and average ratio for 2 days, 5 days, 60 days etc.
for horizon in horizons:
    rolling_averages = sh.rolling(horizon).mean()

    ratio_column = f"Close_Ratio_{horizon}"
    sh[ratio_column] = sh['Close'] / rolling_averages['Close']

    trend_column = f'Trend_{horizon}'
    sh[trend_column] = sh.shift(1).rolling(horizon).sum()['Target']

    new_predictors += [ratio_column, trend_column]

sh = sh.dropna()


#use the RandomForestClassifier model
model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

#this function makes predictions for using the model and the data
def predict(train, test, predictors, model):
    model.fit(train[predictors], train['Target'])
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds >= 0.6] = 1
    preds[preds < 0.6] = 0
    preds = pd.Series(preds, index=test.index, name='Predictions')
    combined = pd.concat([test['Target'], preds], axis=1)
    return combined


predictions = backtest(sh, model, new_predictors)

predictions['Predictions'].value_counts()
#this counts the number of correct predictions and will return the % that it is correct
print(precision_score(predictions['Target'], predictions['Predictions']))




#Ways to improve model:
#Markets open at different times, so track changes in markets to see if these will have an impact on a market about to open
#e.g. Asian markets open before the US market, if Asian markets see a steep rise, will the US market see a rise?
#Use more data
#Add news, interest rate, inflation etc.
#This currently uses daily data, use hourly, minute data?
#Add technical indicators like Moving Averages, Bollinger Bands, RSI, MACD, etc.
#Use other models to see if they perform better instead of Random Forest Classifier - XGBoost, Gradient Boosting, Neural Networks, LightGBM, Support Vector Machines
#use techniques like GridSearchCV or RandomizedSearchCV to find the best hyperparameters for your model.
#Ensemble methods like bagging and boosting can be used to improve the prediction accuracy by combining the outputs of multiple models.
# Time-Series Cross Validation (TSCV) instead of regular cross-validation to validate your model as stock prices have a temporal relationship.
# handling missing values, and removing outliers can improve the performance of the model
#Use a suitable evaluation metric like accuracy, recall, F1-score, etc. in addition to precision_score to get a comprehensive evaluation of the model's performance.
# Increase the training data size to increase the model's accuracy.
#feature importance techniques to identify the most important features and consider removing the less important ones.
# Time-series techniques like ARIMA or LSTMs for better performance with time-series data.
#Handle imbalanced data if present in the target variable by using techniques like oversampling, undersampling, or class weighting.



