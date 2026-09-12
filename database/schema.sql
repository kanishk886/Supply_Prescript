CREATE TABLE IF NOT EXISTS SUPPLYPRESCRIPT_PREDICTIONS (
    prediction_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    model_version_classifier VARCHAR(50),
    model_version_regressor VARCHAR(50),
    predicted_probability FLOAT,
    predicted_duration FLOAT,
    risk_level VARCHAR(20),
    prediction_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SUPPLYPRESCRIPT_OPTIMIZATION_RUNS (
    optimization_run_id VARCHAR(50) PRIMARY KEY,
    prediction_id VARCHAR(50),
    optimal_action VARCHAR(50),
    optimal_score FLOAT,
    execution_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SUPPLYPRESCRIPT_RECOMMENDATIONS (
    recommendation_id VARCHAR(50) PRIMARY KEY,
    optimization_run_id VARCHAR(50),
    action VARCHAR(50),
    expected_cost FLOAT,
    expected_duration FLOAT,
    risk FLOAT,
    objective_score FLOAT,
    feasible BOOLEAN,
    reason VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS SUPPLYPRESCRIPT_DECISIONS (
    decision_id VARCHAR(50) PRIMARY KEY,
    recommendation_id VARCHAR(50),
    prediction_id VARCHAR(50),
    selected_action VARCHAR(50),
    expected_cost FLOAT,
    expected_duration FLOAT,
    optimization_score FLOAT,
    decision_timestamp TIMESTAMP,
    user_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS SUPPLYPRESCRIPT_ACTUAL_OUTCOMES (
    outcome_id VARCHAR(50) PRIMARY KEY,
    decision_id VARCHAR(50),
    actual_duration FLOAT,
    actual_cost FLOAT,
    actual_profit FLOAT,
    outcome_timestamp TIMESTAMP
);
