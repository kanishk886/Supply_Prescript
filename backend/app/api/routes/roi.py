from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ...database.database import get_db
from ...database.models import Decision, Outcome, Prescription

router = APIRouter()

@router.get("/")
def get_roi(db: Session = Depends(get_db)):
    results = db.query(Decision, Outcome, Prescription).join(Outcome, Decision.id == Outcome.decision_id).join(Prescription, Decision.prescription_id == Prescription.id).all()
    
    total_expected_cost = sum(r.Prescription.estimated_cost for r in results) if results else 0
    total_actual_cost = sum(r.Outcome.actual_cost for r in results) if results else 0
    total_profit_saved = sum(r.Outcome.actual_savings for r in results) if results else 0
    
    net_value = total_profit_saved - total_actual_cost
    roi_percentage = (net_value / total_expected_cost * 100) if total_expected_cost > 0 else 0
    
    return {
        "total_decisions_reconciled": len(results),
        "total_expected_cost": total_expected_cost,
        "total_actual_cost": total_actual_cost,
        "total_profit_saved": total_profit_saved,
        "net_value_generated": net_value,
        "roi_percentage": roi_percentage
    }
