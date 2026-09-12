from backend.app.services.db_repository import db_repository
from backend.app.services.writeback_service import writeback_service

def test_save_decision():
    # Make sure local db is initialized
    db_repository.mode = "local"
    db_repository._init_local_db()
    
    decision = {
        "decision_id": "test_dec_1",
        "recommendation_id": "rec_1",
        "prediction_id": "pred_1",
        "selected_action": "EXPEDITED",
        "expected_cost": 15000,
        "expected_duration": 2,
        "optimization_score": 18000,
        "decision_timestamp": "2023-10-01T12:00:00",
        "user_id": "system"
    }
    
    writeback_service.save_decision(decision)
    
    res = db_repository.fetchall("SELECT * FROM SUPPLYPRESCRIPT_DECISIONS WHERE decision_id = 'test_dec_1'")
    assert len(res) == 1
    assert res[0]["selected_action"] == "EXPEDITED"
