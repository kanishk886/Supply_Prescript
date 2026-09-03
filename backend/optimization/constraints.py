def check_constraints(base_cost, expected_duration_adj, risk_adj, max_budget=None, max_acceptable_duration=None, max_acceptable_risk=None):
    """
    Check if a proposed action is feasible under business constraints.
    """
    if max_budget is not None and base_cost > max_budget:
        return False, "Exceeds maximum budget"
        
    if max_acceptable_duration is not None and expected_duration_adj > max_acceptable_duration:
        return False, "Exceeds maximum acceptable duration"
        
    if max_acceptable_risk is not None and risk_adj > max_acceptable_risk:
        return False, "Exceeds maximum acceptable risk"
        
    return True, "Feasible"
