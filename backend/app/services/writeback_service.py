from .db_repository import db_repository
import logging

logger = logging.getLogger(__name__)

class WritebackService:
    def save_prediction(self, pred: dict):
        query = """
        INSERT INTO SUPPLYPRESCRIPT_PREDICTIONS 
        (prediction_id, order_id, model_version_classifier, model_version_regressor, predicted_probability, predicted_duration, risk_level, prediction_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            pred["prediction_id"], pred["order_id"], pred["model_version_classifier"], pred["model_version_regressor"],
            pred["delay_probability"], pred["predicted_duration"], pred["risk_level"], pred["generated_at"]
        )
        db_repository.execute(query, params)

    def save_optimization_run(self, run: dict):
        query = """
        INSERT INTO SUPPLYPRESCRIPT_OPTIMIZATION_RUNS
        (optimization_run_id, prediction_id, optimal_action, optimal_score, execution_timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            run["optimization_run_id"], run["prediction_id"], run["optimal_action"], 
            run["optimal_score"], run["execution_timestamp"]
        )
        db_repository.execute(query, params)
        
        for rec in run["recommendations"]:
            rec_query = """
            INSERT INTO SUPPLYPRESCRIPT_RECOMMENDATIONS
            (recommendation_id, optimization_run_id, action, expected_cost, expected_duration, risk, objective_score, feasible, reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            rec_params = (
                rec["recommendation_id"], rec["optimization_run_id"], rec["action"],
                rec["expected_cost"], rec["expected_duration"], rec["risk"], 
                rec["objective_score"], rec["feasible"], rec["reason"]
            )
            db_repository.execute(rec_query, rec_params)

    def save_decision(self, decision: dict):
        query = """
        INSERT INTO SUPPLYPRESCRIPT_DECISIONS
        (decision_id, recommendation_id, prediction_id, selected_action, expected_cost, expected_duration, optimization_score, decision_timestamp, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            decision["decision_id"], decision["recommendation_id"], decision["prediction_id"], 
            decision["selected_action"], decision["expected_cost"], decision["expected_duration"], 
            decision["optimization_score"], decision["decision_timestamp"], decision.get("user_id", "system")
        )
        db_repository.execute(query, params)

writeback_service = WritebackService()
