# ML Lifecycle & Continuous Learning

## 1. Initial Training
Models are trained using `backend/ml/train_classifier.py` and `backend/ml/train_regressor.py`. Features are extracted from Snowflake (`METRICMIND_DB.PUBLIC.FCT_SALES`).

## 2. Predictions & Optimization
Decisions are generated and logged into the `SUPPLYPRESCRIPT_DECISIONS` table.

## 3. Closed-Loop Reconciliation
The background worker (`backend/worker.py`) constantly matches `DECISIONS` against updated Snowflake data to record actual shipment results into `SUPPLYPRESCRIPT_ACTUAL_OUTCOMES`.

## 4. Automated Retraining
`ContinuousLearningMonitor` runs daily to check:
1. If > 1000 new outcomes have been recorded in the last 7 days.
2. If data or concept drift exceeds thresholds.

If triggered, the system invokes the training pipelines again, creates a new version in `model_metadata.json`, and if evaluation metrics exceed the current active model, seamlessly promotes it.
