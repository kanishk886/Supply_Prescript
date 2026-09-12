# SupplyPrescript Architecture

## Overview
SupplyPrescript is a closed-loop prescriptive analytics system designed to identify supply chain delays and recommend optimal corrective actions, automatically tracking their success and calculating ROI.

## Architecture Components

1. **Data Warehouse (Snowflake)**
   - Houses the `METRICMIND_DB.PUBLIC.FCT_SALES` table.
   - Used for model training and feature extraction.

2. **Machine Learning Pipeline (`backend/ml`)**
   - **Preprocessing**: Cleans data, handles duplicates/dates.
   - **Feature Engineering**: Calculates temporal features, historical modes, and applies one-hot encoding.
   - **Models**:
     - XGBoost Classifier: Predicts probability of shipping delay.
     - XGBoost Regressor: Predicts exact number of delayed days.
   - **Versioning**: Saves metadata and tracks `ACTIVE` and `ARCHIVED` models in `model_metadata.json`.

3. **Prescriptive Optimization Engine (`backend/optimization`)**
   - Combines predictions with business logic constraints.
   - Evaluates actions (Expedited, Alternative, Standard) using a cost/duration/risk objective function.
   - Ranks choices and generates optimization runs.

4. **FastAPI Backend (`backend/app`)**
   - Exposes RESTful endpoints for Predictions, Decisions, Outcomes, and ROI.
   - Uses SQLite/Snowflake dual-mode DB Repository.
   
5. **React Frontend (`frontend`)**
   - Vite + React + TypeScript.
   - **Overview Dashboard**: High-level KPIs and risk charts.
   - **Prescriptive UI**: Presents options (A, B, C) and allows one-click decision execution.
   - **Decision History**: Tracks past decisions and their statuses.
   - **ROI Analytics**: Computes net value generated from avoided penalties.

6. **Closed-Loop Reconciliation (`backend/worker.py`)**
   - Simulates continuous ERP/Snowflake syncing.
   - Records actual outcomes for executed decisions to enable ROI calculation.
   - Sets the stage for continuous model retraining based on new outcomes.
