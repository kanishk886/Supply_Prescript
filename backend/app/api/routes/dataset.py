from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from dateutil import parser
from ...database.database import get_db
from ...database.models import Shipment

router = APIRouter()

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

    # Column Mapping Heuristic
    def map_col(possible_names):
        for col in df.columns:
            if col.strip().lower() in [n.lower() for n in possible_names]:
                return col
        return None

    col_order_id = map_col(['order_id', 'order id', 'id'])
    col_product = map_col(['product', 'item', 'product_name'])
    col_supplier = map_col(['supplier', 'vendor'])
    col_dest = map_col(['destination', 'city', 'location'])
    col_order_date = map_col(['order_date', 'order date', 'date'])
    col_exp_date = map_col(['expected_delivery', 'expected_date', 'expected delivery date'])
    col_act_date = map_col(['actual_delivery', 'actual_date', 'actual delivery date'])
    col_lead = map_col(['lead_time', 'lead time'])
    col_mode = map_col(['shipping_mode', 'shipping mode', 'mode'])
    col_qty = map_col(['quantity', 'qty'])
    col_inv = map_col(['inventory', 'inventory level', 'inventory_level'])
    col_dem = map_col(['demand'])
    col_cost = map_col(['shipping_cost', 'cost'])
    
    def parse_dt(val):
        if pd.isna(val): return None
        try: return parser.parse(str(val))
        except: return None
        
    records_inserted = 0
    for _, row in df.iterrows():
        try:
            order_date = parse_dt(row[col_order_date]) if col_order_date else None
            exp_date = parse_dt(row[col_exp_date]) if col_exp_date else None
            act_date = parse_dt(row[col_act_date]) if col_act_date else None
            
            # Basic delay calculation if missing
            delay_days = None
            if act_date and exp_date:
                delay_days = (act_date - exp_date).days
                if delay_days < 0: delay_days = 0
            
            shipment = Shipment(
                order_id=str(row[col_order_id]) if col_order_id else f"ORD-{records_inserted}",
                product=str(row[col_product]) if col_product else "Unknown",
                supplier=str(row[col_supplier]) if col_supplier else "Unknown",
                destination=str(row[col_dest]) if col_dest else "Unknown",
                order_date=order_date,
                expected_delivery=exp_date,
                actual_delivery=act_date,
                lead_time=int(row[col_lead]) if col_lead and not pd.isna(row[col_lead]) else 0,
                shipping_mode=str(row[col_mode]) if col_mode else "Standard",
                quantity=int(row[col_qty]) if col_qty and not pd.isna(row[col_qty]) else 0,
                inventory=int(row[col_inv]) if col_inv and not pd.isna(row[col_inv]) else 0,
                demand=int(row[col_dem]) if col_dem and not pd.isna(row[col_dem]) else 0,
                shipping_cost=float(row[col_cost]) if col_cost and not pd.isna(row[col_cost]) else 0.0,
                delay_days=delay_days,
                status="Delayed" if delay_days and delay_days > 0 else "On-Time"
            )
            db.add(shipment)
            records_inserted += 1
        except Exception as e:
            continue
            
    db.commit()
    
    return {
        "message": f"Successfully uploaded and processed {records_inserted} records.",
        "rows": len(df),
        "columns": len(df.columns)
    }

@router.delete("/clear")
def clear_dataset(db: Session = Depends(get_db)):
    from ...database.models import Outcome, Decision, Prescription, Prediction
    try:
        db.query(Outcome).delete()
        db.query(Decision).delete()
        db.query(Prescription).delete()
        db.query(Prediction).delete()
        db.query(Shipment).delete()
        db.commit()
        return {"message": "All dataset records have been cleared."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
def dataset_summary(db: Session = Depends(get_db)):
    count = db.query(Shipment).count()
    delayed = db.query(Shipment).filter(Shipment.delay_days > 0).count()
    return {
        "total_shipments": count,
        "delayed_shipments": delayed,
        "on_time_rate": ((count - delayed) / count * 100) if count > 0 else 100
    }
