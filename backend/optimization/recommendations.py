import uuid
from datetime import datetime
from .solver import solver
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def generate_recommendations(self, prediction_id, expected_duration, delay_probability, sales_value, profit_value, business_params):
        logger.info(f"Generating recommendations for prediction {prediction_id}")
        
        results, optimal = solver.solve(
            expected_duration, 
            delay_probability, 
            sales_value, 
            profit_value, 
            business_params
        )
        
        run_id = str(uuid.uuid4())
        
        recommendations = []
        for res in results:
            recommendations.append({
                "recommendation_id": str(uuid.uuid4()),
                "optimization_run_id": run_id,
                "action": res["action_id"],
                "expected_cost": float(res["expected_cost"]),
                "expected_duration": float(res["expected_duration"]),
                "risk": float(res["risk"]),
                "objective_score": float(res["objective_score"]),
                "feasible": res["feasible"],
                "reason": res["reason"],
                "is_optimal": res["action_id"] == optimal["action_id"]
            })
            
        # Rank by objective score
        recommendations.sort(key=lambda x: x["objective_score"])
        
        return {
            "optimization_run_id": run_id,
            "prediction_id": prediction_id,
            "execution_timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "optimal_action": optimal["action_id"],
            "optimal_score": optimal["objective_score"]
        }

recommendation_engine = RecommendationEngine()
