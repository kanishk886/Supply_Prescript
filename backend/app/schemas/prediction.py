from pydantic import BaseModel
from typing import Optional, Dict, Any

class PredictionRequest(BaseModel):
    order_id: str
    order_date: str
    sales: float
    profit: float
    discount: float
    quantity: int
    category: str
    sub_category: str
    shipping_mode: str
    region: str
    segment: str

class PredictionResponse(BaseModel):
    prediction_id: str
    order_id: str
    delay_probability: float
    predicted_duration: float
    risk_level: str
    model_version_classifier: str
    model_version_regressor: str
    generated_at: str
