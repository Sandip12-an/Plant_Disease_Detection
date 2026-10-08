from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer
from backend.app.core.database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(String(100), primary_key=True) # e.g. "Tomato___Early_blight"
    crop = Column(String(100), index=True, nullable=False)
    name = Column(String(150), nullable=False)
    scientific_name = Column(String(150), nullable=True)
    is_healthy = Column(Boolean, default=False)
    description = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=False)
    causes = Column(Text, nullable=True)
    organic_treatment = Column(Text, nullable=False)
    chemical_treatment = Column(Text, nullable=True)
    prevention = Column(Text, nullable=False)
