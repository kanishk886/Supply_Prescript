from pydantic import BaseModel
from typing import Optional

class DecisionRequest(BaseModel):
    recommendation_id: str
    prediction_id: str
    selected_action: str
    expected_cost: float
    expected_duration: float
    optimization_score: float
    user_id: Optional[str] = "system"

class DecisionResponse(BaseModel):
    decision_id: str
    status: str
    message: str

class OutcomeRequest(BaseModel):
    decision_id: str
    actual_duration: float
    actual_cost: float
    actual_profit: float

class OutcomeResponse(BaseModel):
    outcome_id: str
    status: str
