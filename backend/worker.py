import time
import logging
from backend.app.services.reconciliation_service import reconciliation_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_worker():
    logger.info("Starting background reconciliation worker...")
    try:
        while True:
            reconciliation_service.reconcile_outcomes()
            # Sleep for 24 hours in prod, 10 seconds for demo
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Worker stopped.")

if __name__ == "__main__":
    run_worker()
