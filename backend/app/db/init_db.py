import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.core.config import settings
from backend.app.models.disease import Disease
from backend.app.utils.logger import logger

def init_db():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        count = db.query(Disease).count()
        if count == 0:
            logger.info("Seeding diseases knowledge base from JSON...")
            json_path = Path(settings.DISEASE_DATA_PATH)
            if not json_path.exists():
                logger.warning(f"Disease seed data file not found at {json_path}")
                return

            with open(json_path, "r", encoding="utf-8") as f:
                diseases_data = json.load(f)

            for item in diseases_data:
                disease = Disease(
                    id=item["id"],
                    crop=item["crop"],
                    name=item["name"],
                    scientific_name=item.get("scientific_name"),
                    is_healthy=item.get("is_healthy", False),
                    description=item["description"],
                    symptoms=item["symptoms"],
                    causes=item.get("causes"),
                    organic_treatment=item["organic_treatment"],
                    chemical_treatment=item.get("chemical_treatment"),
                    prevention=item["prevention"]
                )
                db.add(disease)
            db.commit()
            logger.info(f"Successfully seeded {len(diseases_data)} disease records into database.")
        else:
            logger.info(f"Database already contains {count} disease records. Skipping seed.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
