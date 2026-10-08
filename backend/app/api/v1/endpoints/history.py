from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.scan import Scan
from backend.app.schemas.scan import ScanResponse, ScanListResponse
from backend.app.api.deps import get_current_user
from backend.app.services.storage_service import StorageService

router = APIRouter()

@router.get("", response_model=ScanListResponse)
def get_scan_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Retrieves paginated scan history. Returns user's scans if authenticated,
    otherwise returns recent public scans.
    """
    query = db.query(Scan)
    if current_user:
        query = query.filter(Scan.user_id == current_user.id)

    total = query.count()
    items = query.order_by(Scan.created_at.desc()).offset(offset).limit(limit).all()

    return {"total": total, "items": items}

@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan_detail(scan_id: str, db: Session = Depends(get_db)):
    """
    Fetches detailed metadata of a specific scan.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan record not found."
        )
    return scan

@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Deletes a scan record and its associated images from storage.
    """
    query = db.query(Scan).filter(Scan.id == scan_id)
    if current_user:
        query = query.filter(Scan.user_id == current_user.id)

    scan = query.first()
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan record not found or unauthorized."
        )

    # Clean up files
    if scan.image_url:
        StorageService.delete_file(scan.image_url.split("/")[-1])
    if scan.heatmap_url:
        StorageService.delete_file(scan.heatmap_url.split("/")[-1])

    db.delete(scan)
    db.commit()
    return None
