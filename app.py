from flask import Flask, render_template, request
import joblib
import os
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Directory to save/load models
MODEL_DIR = 'models'

# Load the best model
def load_best_model():
    best_model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
    model = joblib.load(best_model_path)
    return model

# Preprocess input for prediction
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

            # Load the best model (trained by model_training.py)
            model = load_best_model()

            # Preprocess input
            X_input = preprocess_input(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)

            # Prediction
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
