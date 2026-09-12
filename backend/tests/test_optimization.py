from backend.optimization.solver import solver
from backend.optimization.recommendations import recommendation_engine

def test_solver():
    results, optimal = solver.solve(
        expected_duration=14.0,
        delay_probability=0.87,
        sales_value=2000,
        profit_value=500,
        business_params={"max_budget": 10000}
    )
    
    assert len(results) == 3
    assert optimal is not None
    assert optimal["feasible"] is True

def test_recommendation_engine():
    res = recommendation_engine.generate_recommendations(
        prediction_id="pred_123",
        expected_duration=14.0,
        delay_probability=0.87,
        sales_value=2000,
        profit_value=500,
        business_params={"max_budget": 10000}
    )
    
    assert res["prediction_id"] == "pred_123"
    assert len(res["recommendations"]) == 3
    
    # Check that it's ranked
    scores = [r["objective_score"] for r in res["recommendations"]]
    assert scores == sorted(scores)
