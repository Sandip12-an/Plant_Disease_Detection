import os
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plant Disease Detection System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "temporary-insecure-dev-secret-key-plant-disease-detection-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Base workspace directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

    # Database
    DATABASE_URL: str = "sqlite:///./plant_disease.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Storage & Uploads
    UPLOAD_DIR: str = str(Path(__file__).resolve().parent.parent.parent / "uploads")
    MAX_UPLOAD_SIZE_MB: int = 15

    # ML Model & Knowledge Base Artifacts
    MODEL_PATH: str = str(Path(__file__).resolve().parent.parent.parent.parent / "ml" / "model_registry" / "mobilenet_v2_v1.onnx")
    CLASS_LABELS_PATH: str = str(Path(__file__).resolve().parent.parent.parent.parent / "ml" / "model_registry" / "class_labels.json")
    DISEASE_DATA_PATH: str = str(Path(__file__).resolve().parent.parent / "db" / "seed_data" / "diseases_data.json")
    CONFIDENCE_THRESHOLD: float = 0.50

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure uploads directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
