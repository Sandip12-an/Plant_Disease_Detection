from typing import List, Optional
from pydantic import BaseModel

class TreatmentPlan(BaseModel):
    crop: str
    disease_name: str
    is_healthy: bool
    description: str
    symptoms: str
    organic_treatment: str
    chemical_treatment: Optional[str] = None
    prevention: str

class TopClassPrediction(BaseModel):
    disease_class: str
    crop: str
    disease_name: str
    confidence: float
    percentage: str

class PredictionResponse(BaseModel):
    scan_id: str
    crop: str
    disease: str
    disease_class: str
    confidence: float
    is_healthy: bool
    severity: str
    original_image_url: str
    heatmap_url: Optional[str] = None
    treatment: TreatmentPlan
    top_predictions: List[TopClassPrediction]
    warning: Optional[str] = None
