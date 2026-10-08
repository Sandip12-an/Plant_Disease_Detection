import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    image_url = Column(String(512), nullable=False)
    heatmap_url = Column(String(512), nullable=True)
    crop_name = Column(String(100), nullable=False)
    disease_name = Column(String(150), nullable=False)
    disease_class = Column(String(150), nullable=False)
    confidence = Column(Float, nullable=False)
    is_healthy = Column(Boolean, default=False)
    treatment_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scans")
