from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine
from .database import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupplyPrescript API",
    description="Closed-Loop Prescriptive Analytics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .api.routes import predictions, decisions, roi, auth, chat, dataset

app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])
app.include_router(roi.router, prefix="/api/roi", tags=["roi"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(dataset.router, prefix="/api/dataset", tags=["dataset"])

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": app.version}
