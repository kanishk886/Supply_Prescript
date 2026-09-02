from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.models import Shipment, Prediction
from backend.ml.predict import prediction_service

router = APIRouter()

@router.post("/predict/{shipment_id}")
def predict_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    features = {
        "lead_time": shipment.lead_time,
        "quantity": shipment.quantity,
        "inventory": shipment.inventory,
        "demand": shipment.demand,
        "shipping_cost": shipment.shipping_cost
    }

    try:
        # Pass necessary data as dict matching the original prediction_service format
        input_data = {
            "order_id": shipment.order_id,
            "order_date": shipment.order_date,
            "lead_time": shipment.lead_time,
            "quantity": shipment.quantity,
            "inventory": shipment.inventory,
            "demand": shipment.demand,
            "shipping_cost": shipment.shipping_cost,
            "product": shipment.product,
            "supplier": shipment.supplier,
            "shipping_mode": shipment.shipping_mode,
            "destination": shipment.destination,
        }
        
        result = prediction_service.predict(input_data)
        
        # Save prediction
        prediction = Prediction(
            shipment_id=shipment.id,
            delay_probability=result['delay_probability'],
            predicted_delay_days=result['predicted_duration'],
            model_version=result['model_version_classifier']
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risks")
def get_supply_risks(db: Session = Depends(get_db)):
    results = db.query(Prediction, Shipment).join(
        Shipment, Prediction.shipment_id == Shipment.id
    ).order_by(Prediction.delay_probability.desc()).limit(100).all()
    
    data = []
    for p, s in results:
        risk_level = "High" if p.delay_probability > 0.7 else ("Medium" if p.delay_probability > 0.4 else "Low")
        data.append({
            "id": p.id,
            "shipment_id": s.id,
            "order_id": s.order_id,
            "product": s.product,
            "supplier": s.supplier,
            "destination": s.destination,
            "delay_probability": round(p.delay_probability * 100, 1),
            "predicted_delay": p.predicted_delay_days,
            "inventory": s.inventory,
            "demand": s.demand,
            "risk": risk_level
        })
    return data
