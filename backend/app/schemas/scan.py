from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ScanBase(BaseModel):
    crop_name: str
    disease_name: str
    disease_class: str
    confidence: float
    is_healthy: bool
    image_url: str
    heatmap_url: Optional[str] = None
    treatment_summary: Optional[str] = None

class ScanCreate(ScanBase):
    user_id: Optional[str] = None

class ScanResponse(ScanBase):
    id: str
    user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ScanListResponse(BaseModel):
    total: int
    items: List[ScanResponse]
