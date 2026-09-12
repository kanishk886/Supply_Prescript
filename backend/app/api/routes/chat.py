from fastapi import APIRouter, Depends
from pydantic import BaseModel
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import func
from ...database.database import get_db
from ...database.models import Shipment, Decision, Outcome

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    shipment_id: int = None

class ChatResponse(BaseModel):
    answer: str

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

def get_context(db: Session, shipment_id: int = None):
    context = "You are the SupplyPrescript AI Assistant. "
    
    if shipment_id:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if shipment:
            context += f"""
            You are explaining recommendations for Shipment {shipment.order_id}.
            Product: {shipment.product}
            Supplier: {shipment.supplier}
            Predicted Delay: {shipment.delay_days} days.
            Shipping Cost: ${shipment.shipping_cost}.
            Inventory: {shipment.inventory} vs Demand: {shipment.demand}.
            Explain the trade-offs between Air Freight (fast but expensive), Secondary Supplier (moderate), and Reschedule (cheap but delayed).
            Never invent numerical data.
            """
            return context
            
    # Generic stats
    dec_cnt = db.query(Decision).count()
    risk_cnt = db.query(Shipment).filter(Shipment.delay_days > 0).count()
    
    context += f"""
    Current System Context:
    - Total executed decisions: {dec_cnt}
    - Current shipments flagged as High Risk: {risk_cnt}
    
    Answer the user's question concisely using ONLY this data. If explaining a prediction or action, emphasize the business trade-off between cost and delay.
    """
    return context

@router.post("/query", response_model=ChatResponse)
async def ask_question(request: ChatRequest, db: Session = Depends(get_db)):
    context = get_context(db, request.shipment_id)
    prompt = f"{context}\n\nUser Question: {request.query}\nAnswer:"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0
            )
            if response.status_code == 200:
                return {"answer": response.json().get("response", "No response.")}
            else:
                return {"answer": f"Ollama Error. Ensure {OLLAMA_MODEL} is pulled."}
    except Exception:
        return {"answer": "Ollama is not reachable. Please start the Ollama service."}
