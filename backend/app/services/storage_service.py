import os
import uuid
from pathlib import Path
from PIL import Image
from backend.app.core.config import settings
from backend.app.utils.logger import logger

class StorageService:
    @staticmethod
    def save_image(image: Image.Image, prefix: str = "leaf") -> str:
        """
        Saves PIL Image to upload directory with unique filename.
        Returns the filename.
        """
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        filename = f"{prefix}_{uuid.uuid4().hex[:12]}.jpg"
        filepath = Path(settings.UPLOAD_DIR) / filename
        image.save(filepath, format="JPEG", quality=92)
        logger.info(f"Image saved to storage: {filename}")
        return filename

    @staticmethod
    def delete_file(filename: str):
        """
        Removes file from storage directory if exists.
        """
        try:
            filepath = Path(settings.UPLOAD_DIR) / filename
            if filepath.exists():
                os.remove(filepath)
                logger.info(f"Deleted file: {filename}")
        except Exception as e:
            logger.warning(f"Error deleting file {filename}: {e}")
