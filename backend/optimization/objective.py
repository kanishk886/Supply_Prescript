import numpy as np

def calculate_operational_cost(action_index, expected_duration, delay_probability, sales_value, profit_value,
                               cost_expedited=0, cost_alternative=0, delay_penalty_per_day=0, service_level_threshold=3):
    """
    Objective function to MINIMIZE TOTAL OPERATIONAL COST.
    action_index: 0 (Expedited), 1 (Alternative), 2 (Standard)
    """
    
    # Base costs based on action
    if action_index == 0:
        base_cost = cost_expedited
        expected_duration_adj = max(1, expected_duration * 0.3) # 70% reduction
        risk_adj = delay_probability * 0.1
    elif action_index == 1:
        base_cost = cost_alternative
        expected_duration_adj = max(2, expected_duration * 0.6) # 40% reduction
        risk_adj = delay_probability * 0.5
    else:
        base_cost = 0
        expected_duration_adj = expected_duration
        risk_adj = delay_probability
        
    # Penalty if duration exceeds service level
    delay_days = max(0, expected_duration_adj - service_level_threshold)
    delay_penalty = delay_days * delay_penalty_per_day
    
    # Expected profit impact (risk of cancellation/refund)
    # Higher risk -> higher chance of losing profit or getting penalized
    expected_profit_impact = risk_adj * profit_value * 0.5 # Assume 50% profit loss on risk realization
    
    total_cost = base_cost + delay_penalty + expected_profit_impact
    
    return total_cost, expected_duration_adj, risk_adj, base_cost
