import joblib
import pandas as pd
import logging
from datetime import datetime
import uuid
import os

from .versioning import version_manager
from .feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.clf_data = self._load_model('xgboost_classifier.joblib')
        self.reg_data = self._load_model('xgboost_regressor.joblib')
        self.fe = FeatureEngineer()
        
    def _load_model(self, filename):
        path = os.path.join("models", filename)
        if os.path.exists(path):
            return joblib.load(path)
        logger.warning(f"Model not found at {path}")
        return None

    def predict(self, input_data: dict) -> dict:
        if not self.clf_data or not self.reg_data:
            raise ValueError("Models are not loaded.")

        # Convert input to DataFrame
        df = pd.DataFrame([input_data])
        df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Missing dummy columns like historical_mode_duration
        df['shipping_delay_days'] = 0 # Dummy target for FE
        df['historical_mode_duration'] = 4.0 # Default/imputed
        df['historical_mode_delay_rate'] = 0.5 # Default/imputed
        
        # Feature engineering
        df_feat = self.fe.transform(df)
        
        # Align features for classifier
        clf_features = self.clf_data["features"]
        X_clf = pd.DataFrame(columns=clf_features)
        for col in clf_features:
            if col in df_feat.columns:
                X_clf[col] = df_feat[col]
            else:
                X_clf[col] = 0
                
        # Align features for regressor
        reg_features = self.reg_data["features"]
        X_reg = pd.DataFrame(columns=reg_features)
        for col in reg_features:
            if col in df_feat.columns:
                X_reg[col] = df_feat[col]
            else:
                X_reg[col] = 0

        # Predict
        prob = self.clf_data["model"].predict_proba(X_clf)[0, 1]
        duration = self.reg_data["model"].predict(X_reg)[0]
        
        risk_level = "High" if prob > 0.7 else ("Medium" if prob > 0.4 else "Low")
        
        # Get active model versions
        clf_version = version_manager.get_active_model("classifier")
        reg_version = version_manager.get_active_model("regressor")

        return {
            "prediction_id": str(uuid.uuid4()),
            "order_id": input_data["order_id"],
            "delay_probability": float(prob),
            "predicted_duration": float(duration),
            "risk_level": risk_level,
            "model_version_classifier": clf_version["model_version"] if clf_version else "UNKNOWN",
            "model_version_regressor": reg_version["model_version"] if reg_version else "UNKNOWN",
            "generated_at": datetime.now().isoformat()
        }

prediction_service = PredictionService()
