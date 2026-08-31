import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import logging

from backend.app.database.database import engine
from backend.ml.versioning import version_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_classifier():
    logger.info("Extracting data from SQLite Shipments table...")
    df = pd.read_sql("SELECT * FROM shipments", con=engine)
    
    if len(df) < 10:
        logger.warning("Not enough data to train model.")
        return

    # Basic feature engineering
    df['is_delayed'] = (df['delay_days'] > 0).astype(int)
    
    # Select features
    features = ['lead_time', 'quantity', 'inventory', 'demand', 'shipping_cost']
    X = df[features].fillna(0)
    y = df['is_delayed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    preds_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "f1": f1_score(y_test, preds, zero_division=0),
        "roc_auc": roc_auc_score(y_test, preds_proba)
    }
    logger.info(f"Classifier Metrics: {metrics}")

    joblib.dump({"model": model, "features": features}, "models/xgboost_classifier.joblib")
    version_manager.register_model("classifier", metrics, features)
    logger.info("Model saved successfully.")

if __name__ == "__main__":
    train_classifier()
