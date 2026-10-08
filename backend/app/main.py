import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.core.config import settings
from backend.app.api.v1.router import api_router
from backend.app.db.init_db import init_db
from backend.app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """
    logger.info("Starting Plant Disease Detection API...")
    init_db()
    yield
    logger.info("Shutting down Plant Disease Detection API.")

# Ensure DB is ready on import (essential for test runners and synchronous clients)
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="High-performance AI platform for crop leaf disease diagnosis, Grad-CAM explainability, and agronomic treatment guidance.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static uploads directory for serving leaf and Grad-CAM images
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include v1 API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def root_status():
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "api_docs": "/docs",
        "health_check": f"{settings.API_V1_STR}/health",
        "version": "1.0.0"
    }
