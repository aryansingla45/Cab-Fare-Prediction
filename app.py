from flask import Flask, render_template, request, redirect, url_for
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Directory to save/load models
MODEL_DIR = 'models'

def load_train_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['pickup_datetime'])
    return df

def preprocess_data(df):
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.weekday
    X = df[['pickup_hour', 'pickup_day_of_week', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']]
    return X

def train_model(X, y, model_type='linear'):
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_path = os.path.join(MODEL_DIR, f"{model_type}_model.pkl")
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        if model_type == 'linear':
            model = LinearRegression()
        else:
            raise ValueError("Invalid model type")
        model.fit(X, y)
        joblib.dump(model, model_path)
    return model

def preprocess_input(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    pickup_datetime = datetime.strptime(pickup_datetime, '%Y-%m-%dT%H:%M')
    pickup_hour = pickup_datetime.hour
    pickup_day_of_week = pickup_datetime.weekday()
    X = [[pickup_hour, pickup_day_of_week, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count]]
    return X

def predict_fare_amount(X, model):
    fare_amount = model.predict(X)
    return fare_amount

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            # Extract form data
            pickup_datetime = request.form['pickup_datetime']
            pickup_longitude = float(request.form['pickup_longitude'])
            pickup_latitude = float(request.form['pickup_latitude'])
            dropoff_longitude = float(request.form['dropoff_longitude'])
            dropoff_latitude = float(request.form['dropoff_latitude'])
            passenger_count = int(request.form['passenger_count'])
            model_type = request.form['model_type']

            # Training
            train_file_path = 'train.csv'
            train_df = load_train_data(train_file_path)
            X_train = preprocess_data(train_df)
            y_train = train_df['fare_amount']
            model = train_model(X_train, y_train, model_type)

            # Prediction
            X_input = preprocess_input(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)
            fare_amount = predict_fare_amount(X_input, model)
            fare_amount = (fare_amount * passenger_count).tolist()

            return render_template('predict.html', fare="Fare = ${:.2f}".format(fare_amount[0]))
        except Exception as e:
            return str(e)
    elif request.method == 'GET':
        # Render the predict.html page for a GET request
        return render_template('predict.html', fare=None)


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
