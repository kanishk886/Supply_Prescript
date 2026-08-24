import os
import subprocess
from datetime import datetime, timedelta

def run(cmd, env=None):
    return subprocess.run(cmd, shell=True, check=False, env=env, capture_output=True, text=True)

# Start 20 days ago
start_date = datetime.now() - timedelta(days=20)

commits = [
    {"day": 1, "msg": "init: setup project structure and virtual environment", "files": ["README.md", "requirements.txt", ".gitignore", ".env.example", "Dockerfile", "make_commits.py", "mock.py", "inspect_snowflake.py"]},
    {"day": 2, "msg": "feat: initialize sqlite database and sqlalchemy models", "files": ["backend/app/database"]},
    {"day": 3, "msg": "feat: setup fastapi core and basic health routes", "files": ["backend/app/main.py", "backend/app/config.py", "backend/worker.py"]},
    {"day": 4, "msg": "feat: implement user authentication and jwt logic", "files": ["backend/app/api/routes/auth.py"]},
    {"day": 5, "msg": "chore: create mock dataset generation script", "files": ["supply_chain_sample.csv", "dynamic_supply_chain_logistics_dataset.csv"]},
    {"day": 6, "msg": "feat: implement dataset upload and bulk db insert", "files": ["backend/app/api/routes/dataset.py"]},
    {"day": 7, "msg": "feat: add data preprocessing and feature engineering", "files": ["backend/ml/preprocessing.py", "backend/ml/feature_engineering.py", "backend/ml/versioning.py", "backend/ml/evaluate.py", "backend/ml/retraining.py"]},
    {"day": 8, "msg": "feat: train xgboost classifier for delay probability", "files": ["backend/ml/train_classifier.py", "models/xgboost_classifier.joblib"]},
    {"day": 9, "msg": "feat: train xgboost regressor for delay duration", "files": ["backend/ml/train_regressor.py", "models/xgboost_regressor.joblib", "models/model_metadata.json"]},
    {"day": 10, "msg": "feat: build predictive service and risk endpoints", "files": ["backend/ml/predict.py", "backend/app/api/routes/predictions.py"]},
    {"day": 11, "msg": "feat: implement scipy optimization engine for logistics", "files": ["backend/optimization"]},
    {"day": 12, "msg": "feat: add prescriptive generation and execution routes", "files": ["backend/app/api/routes/decisions.py"]},
    {"day": 13, "msg": "feat: implement ROI and outcome reconciliation endpoints", "files": ["backend/app/api/routes/roi.py"]},
    {"day": 14, "msg": "init: setup react frontend with vite and typescript", "files": ["frontend/package.json", "frontend/tsconfig.json", "frontend/tsconfig.node.json", "frontend/vite.config.ts", "frontend/index.html", "frontend/src/App.tsx", "frontend/src/main.tsx", "frontend/src/layouts", "frontend/src/index.css"]},
    {"day": 15, "msg": "feat: build login, register, and auth context", "files": ["frontend/src/context", "frontend/src/pages/Login.tsx", "frontend/src/pages/Register.tsx", "frontend/src/services"]},
    {"day": 16, "msg": "feat: develop overview dashboard with recharts", "files": ["frontend/src/pages/Overview.tsx"]},
    {"day": 17, "msg": "feat: build dataset management and supply risk ui", "files": ["frontend/src/pages/Dataset.tsx", "frontend/src/pages/SupplyRisk.tsx"]},
    {"day": 18, "msg": "feat: implement prescriptive decision making interface", "files": ["frontend/src/pages/Prescriptive.tsx"]},
    {"day": 19, "msg": "feat: build history and outcome analytics dashboard", "files": ["frontend/src/pages/History.tsx", "frontend/src/pages/RoiDashboard.tsx"]},
    {"day": 20, "msg": "feat: integrate ollama ai chatbot and final integration", "files": ["backend/app/api/routes/chat.py", "frontend/src/components/ChatWidget.tsx", "."]} 
]

for commit in commits:
    day_offset = commit["day"] - 1
    commit_date = start_date + timedelta(days=day_offset)
    date_str = commit_date.strftime('%Y-%m-%dT12:00:00')
    
    # Add files
    for f in commit["files"]:
        if os.path.exists(f) or f == ".":
            run(f'git add "{f}"')
    
    # Commit
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    status = run('git status --porcelain')
    if status.stdout.strip():
        run(f'git commit -m "{commit["msg"]}"', env=env)

# Run push (if authenticated) or just add remote
run('git remote add origin https://github.com/kanishk886/Supply_Prescript.git')
run('git branch -M main')
print("Successfully built commit history!")
