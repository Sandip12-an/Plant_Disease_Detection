from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, auth, predict, history, diseases

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(predict.router, tags=["Diagnosis & Prediction"])
api_router.include_router(history.router, prefix="/history", tags=["Scan History"])
api_router.include_router(diseases.router, prefix="/diseases", tags=["Disease Directory & Remedies"])
