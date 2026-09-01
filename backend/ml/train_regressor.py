import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import logging

from backend.app.database.database import engine
from backend.ml.versioning import version_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_regressor():
    logger.info("Extracting data from SQLite Shipments table...")
    df = pd.read_sql("SELECT * FROM shipments WHERE delay_days > 0", con=engine)
    
    if len(df) < 10:
        logger.warning("Not enough delayed shipments to train regressor.")
        return

    features = ['lead_time', 'quantity', 'inventory', 'demand', 'shipping_cost']
    X = df[features].fillna(0)
    y = df['delay_days']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info("Training XGBoost Regressor...")
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, preds),
        "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
        "r2": r2_score(y_test, preds)
    }
    logger.info(f"Regressor Metrics: {metrics}")

    joblib.dump({"model": model, "features": features}, "models/xgboost_regressor.joblib")
    version_manager.register_model("regressor", metrics, features)
    logger.info("Regressor saved successfully.")

if __name__ == "__main__":
    train_regressor()
