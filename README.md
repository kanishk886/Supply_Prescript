# Supply Prescript – Closed-Loop Prescriptive Analytics

Supply Prescript is an enterprise-grade, closed-loop analytics application designed to predict supply chain delays and recommend optimal actions using Machine Learning (XGBoost) and Mathematical Optimization (SciPy). It includes a fully functional write-back architecture to track decision outcomes and calculate Return on Investment (ROI).

## Features
- **Dataset Ingestion**: Upload custom CSV datasets (Pandas mapping).
- **Predictive ML**: XGBoost models predict delay probabilities.
- **Prescriptive Optimization**: SciPy optimization dynamically generates options (Air Freight, Secondary Supplier, Reschedule) balancing cost, speed, and risk.
- **Write-back Architecture**: Executes decisions to the SQLAlchemy database and tracks actual outcomes.
- **AI Assistant**: RAG-enabled chat powered by local **Ollama (llama3)** for business explanations.
- **Secure Authentication**: Passlib/bcrypt password hashing and JWT sessions.

## Tech Stack
- **Frontend**: React, TypeScript, Vite
- **Backend**: FastAPI, SQLAlchemy (SQLite/PostgreSQL compatible)
- **ML / AI**: XGBoost, Scikit-learn, SciPy, Pandas, Ollama

## Installation (Windows)

### 1. Backend Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Ollama Setup
Ensure you have [Ollama](https://ollama.com/) installed and running locally.
```bash
ollama run llama3
```

## Workflow Guide
1. **Register & Login**: Create a secure account.
2. **Dataset**: Navigate to the Dataset page and upload your historical supply chain CSV.
3. **ML Training**: Run the background XGBoost training scripts (`python -m backend.ml.train_classifier`).
4. **Prescriptions**: View High Risk shipments and select dynamically generated optimal actions.
5. **Decisions**: Execute decisions, which write to the DB.
6. **Analytics**: The reconciliation worker tracks the executed decisions to display actual ROI on the dashboard.
7. **Chat**: Use the bottom right chat widget to ask Ollama to explain recommendations.

## API Documentation
Once the backend is running, visit: `http://localhost:8000/docs`
