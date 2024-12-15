import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import os
import lightgbm as lgb

# Directory to save the model
MODEL_DIR = 'models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Load and preprocess the data
def load_train_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['pickup_datetime'])
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.weekday
    X = df[['pickup_hour', 'pickup_day_of_week', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']]
    y = df['fare_amount']
    return X, y

# Train models and evaluate them
def train_and_evaluate_models(X, y):
    models = {
        "linear": LinearRegression(),
        "decision_tree": DecisionTreeRegressor(),
        "random_forest": RandomForestRegressor(),
        "gradient_boosting": GradientBoostingRegressor(),
        "svm": SVR(),
        "knn": KNeighborsRegressor(),
        "xgboost": xgb.XGBRegressor(),
        "lightgbm": lgb.LGBMRegressor()
    }

    best_model = None
    best_score = float('inf')

    for model_name, model in models.items():
        model.fit(X, y)
        y_pred = model.predict(X)
        score = mean_squared_error(y, y_pred)  # You can also use R² here if needed
        print(f"Model: {model_name}, MSE: {score}")

        if score < best_score:
            best_score = score
            best_model = model
            best_model_name = model_name

    # Save the best model
    model_path = os.path.join(MODEL_DIR, f"best_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"Best model: {best_model_name} saved to {model_path}")

if __name__ == "__main__":
    # Assuming the training data is in 'train.csv'
    train_file_path = 'train.csv'
    X_train, y_train = load_train_data(train_file_path)
    train_and_evaluate_models(X_train, y_train)
