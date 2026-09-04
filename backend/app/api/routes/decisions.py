from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.models import Shipment, Prediction, Prescription, Decision, Outcome
from backend.optimization.solver import optimization_engine

router = APIRouter()

@router.post("/generate/{shipment_id}")
def generate_prescriptions(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
        
    prediction = db.query(Prediction).filter(Prediction.shipment_id == shipment_id).order_by(Prediction.id.desc()).first()
    predicted_delay = prediction.predicted_delay_days if prediction else 10
    
    options = optimization_engine.generate_options(shipment.shipping_cost, predicted_delay)
    
    saved_options = []
    for opt in options:
        prescription = Prescription(
            shipment_id=shipment.id,
            **opt
        )
        db.add(prescription)
        saved_options.append(prescription)
        
    db.commit()
    for opt in saved_options:
        db.refresh(opt)
        
    return saved_options

@router.post("/execute")
def execute_decision(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
        
    decision = Decision(
        prescription_id=prescription.id,
        user_id=1, # Default user for now until auth integration
        selected_action=prescription.action_type
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return {"message": "Decision successfully recorded.", "decision_id": decision.id}

@router.get("/")
def get_decisions(db: Session = Depends(get_db)):
    results = db.query(Decision, Prescription, Shipment).join(
        Prescription, Decision.prescription_id == Prescription.id
    ).join(
        Shipment, Prescription.shipment_id == Shipment.id
    ).order_by(Decision.decision_date.desc()).all()
    
    data = []
    for d, p, s in results:
        outcome = db.query(Outcome).filter(Outcome.decision_id == d.id).first()
        status = "PENDING OUTCOME"
        if outcome:
            status = "SUCCESS" if outcome.success else "DELAYED"
            
        data.append({
            "id": d.id,
            "date": d.decision_date.strftime("%Y-%m-%d %H:%M"),
            "orderId": s.order_id,
            "action": d.selected_action,
            "status": status
        })
    return data
