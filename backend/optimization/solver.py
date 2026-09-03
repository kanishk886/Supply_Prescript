from scipy.optimize import minimize
import logging

logger = logging.getLogger(__name__)

class OptimizationEngine:
    def generate_options(self, shipment_cost, predicted_delay):
        """
        Dynamically calculates 3 alternatives based on the base shipment cost and delay.
        """
        base_cost = shipment_cost if shipment_cost > 0 else 5000
        base_delay = predicted_delay if predicted_delay > 0 else 5
        
        options = []
        
        # Option A: Expedited / Air Freight
        # Higher cost (+200%), Faster delivery (-80% delay), Low risk
        options.append({
            "option_name": "OPTION A",
            "action_type": "Expedited Shipping",
            "estimated_cost": base_cost * 3.0,
            "estimated_delay": max(1, base_delay * 0.2),
            "risk_score": 0.1,
            "expected_savings": (base_delay * 500) - (base_cost * 2.0), # Assuming $500 penalty per delay day
            "optimization_score": 90.0
        })
        
        # Option B: Secondary Supplier
        # Moderate cost (+50%), Moderate delivery (-50% delay), Medium risk
        options.append({
            "option_name": "OPTION B",
            "action_type": "Secondary Supplier",
            "estimated_cost": base_cost * 1.5,
            "estimated_delay": max(1, base_delay * 0.5),
            "risk_score": 0.3,
            "expected_savings": (base_delay * 500 * 0.5) - (base_cost * 0.5),
            "optimization_score": 75.0
        })
        
        # Option C: Standard / Reschedule
        # No extra cost, Full delay, High business risk
        options.append({
            "option_name": "OPTION C",
            "action_type": "Standard Reschedule",
            "estimated_cost": base_cost,
            "estimated_delay": base_delay,
            "risk_score": 0.8,
            "expected_savings": 0,
            "optimization_score": 30.0
        })
        
        return options

optimization_engine = OptimizationEngine()
