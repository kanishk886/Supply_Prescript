from backend.optimization.solver import optimization_engine

def test_optimization_engine():
    results = optimization_engine.generate_options(
        shipment_cost=2000,
        predicted_delay=14.0
    )
    
    assert len(results) == 3
    assert results[0]["action_type"] == "Expedited Shipping"
    assert results[1]["action_type"] == "Secondary Supplier"
    assert results[2]["action_type"] == "Standard Reschedule"

