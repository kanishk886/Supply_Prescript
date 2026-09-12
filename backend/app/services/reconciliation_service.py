import logging
import uuid
import random
from datetime import datetime
from .db_repository import db_repository
from backend.app.database.database import SessionLocal
from backend.app.database.models import Decision, Outcome, Prescription

logger = logging.getLogger(__name__)

class ReconciliationService:
    def reconcile_outcomes(self):
        logger.info("Starting closed-loop reconciliation via SQLAlchemy...")
        
        db = SessionLocal()
        try:
            # Find decisions without outcomes
            pending = db.query(Decision).outerjoin(Outcome).filter(Outcome.id == None).all()
            
            reconciled = 0
            for decision in pending:
                prescription = db.query(Prescription).filter(Prescription.id == decision.prescription_id).first()
                if not prescription: continue
                
                # Simulate actuals
                actual_delay = prescription.estimated_delay + random.randint(-1, 3)
                actual_cost = prescription.estimated_cost + random.uniform(-500, 1500)
                actual_savings = prescription.expected_savings + random.uniform(-1000, 1000)
                
                outcome = Outcome(
                    decision_id=decision.id,
                    actual_cost=max(0, actual_cost),
                    actual_delay=max(0, actual_delay),
                    actual_savings=actual_savings,
                    success=(actual_delay <= prescription.estimated_delay + 1)
                )
                db.add(outcome)
                reconciled += 1
                
            db.commit()
            logger.info(f"Reconciled {reconciled} pending decisions with actual outcomes.")
            return reconciled
        except Exception as e:
            logger.error(f"Reconciliation error: {e}")
        finally:
            db.close()

reconciliation_service = ReconciliationService()
