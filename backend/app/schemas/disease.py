from typing import Optional, List
from pydantic import BaseModel

class DiseaseBase(BaseModel):
    id: str
    crop: str
    name: str
    scientific_name: Optional[str] = None
    is_healthy: bool
    description: str
    symptoms: str
    causes: Optional[str] = None
    organic_treatment: str
    chemical_treatment: Optional[str] = None
    prevention: str

class DiseaseResponse(DiseaseBase):
    class Config:
        from_attributes = True

class DiseaseListResponse(BaseModel):
    total: int
    items: List[DiseaseResponse]
