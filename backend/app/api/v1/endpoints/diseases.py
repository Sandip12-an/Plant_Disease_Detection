from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.core.database import get_db
from backend.app.models.disease import Disease
from backend.app.schemas.disease import DiseaseResponse, DiseaseListResponse

router = APIRouter()

@router.get("/crops", response_model=List[str])
def get_crop_list(db: Session = Depends(get_db)):
    """
    Returns unique list of crop species covered in the system.
    """
    crops = db.query(Disease.crop).distinct().all()
    return sorted([c[0] for c in crops if c[0]])

@router.get("", response_model=DiseaseListResponse)
def list_diseases(
    crop: Optional[str] = Query(None, description="Filter by crop species"),
    search: Optional[str] = Query(None, description="Search by disease or symptom"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Returns a searchable directory of plant diseases and healthy benchmarks.
    """
    query = db.query(Disease)

    if crop:
        query = query.filter(Disease.crop.ilike(f"%{crop}%"))

    if search:
        query = query.filter(
            (Disease.name.ilike(f"%{search}%")) |
            (Disease.symptoms.ilike(f"%{search}%")) |
            (Disease.description.ilike(f"%{search}%"))
        )

    total = query.count()
    items = query.order_by(Disease.crop.asc(), Disease.name.asc()).offset(offset).limit(limit).all()

    return {"total": total, "items": items}

@router.get("/{disease_id}", response_model=DiseaseResponse)
def get_disease_detail(disease_id: str, db: Session = Depends(get_db)):
    """
    Returns comprehensive agronomic disease profile, symptoms,
    organic remedies, and chemical treatment guidelines.
    """
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease '{disease_id}' not found in knowledge base."
        )
    return disease
