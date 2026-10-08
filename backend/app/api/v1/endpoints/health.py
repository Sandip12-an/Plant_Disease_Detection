from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.database import get_db
from backend.app.services.inference_service import inference_engine
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", summary="Health and Model Readiness Probe")
def health_check(db: Session = Depends(get_db)):
    """
    Returns system liveness, database status, and inference model readiness.
    """
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    model_ready = inference_engine.session is not None
    classes_loaded = len(inference_engine.class_labels)

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": settings.PROJECT_NAME,
        "database": db_status,
        "model_engine": {
            "ready": model_ready or classes_loaded > 0,
            "runtime": "onnxruntime" if model_ready else "fallback_heuristic",
            "classes_registered": classes_loaded,
            "architecture": "MobileNetV2"
        },
        "version": "1.0.0"
    }
