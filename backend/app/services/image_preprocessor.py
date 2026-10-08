import io
import numpy as np
from PIL import Image
from typing import Tuple
from backend.app.core.config import settings
from backend.app.utils.exceptions import InvalidImageError
from backend.app.utils.logger import logger

class ImagePreprocessor:
    ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}
    TARGET_SIZE = (224, 224)
    IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    @classmethod
    def validate_and_load(cls, file_bytes: bytes) -> Image.Image:
        """
        Validates file integrity, format, and loads as PIL Image.
        """
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(file_bytes) > max_bytes:
            raise InvalidImageError(f"Image exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB}MB")

        try:
            image = Image.open(io.BytesIO(file_bytes))
            image.verify() # Verify file header and integrity
            # Re-open because verify() closes the stream
            image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        except Exception as e:
            logger.warning(f"Image validation failed: {e}")
            raise InvalidImageError("Could not decode image. Please upload a valid JPG or PNG file.")

        return image

    @classmethod
    def preprocess_for_inference(cls, image: Image.Image) -> np.ndarray:
        """
        Resizes to (224, 224), normalizes with ImageNet statistics,
        and converts to NCHW format [1, 3, 224, 224] for ONNX runtime.
        """
        resized = image.resize(cls.TARGET_SIZE, Image.Resampling.BILINEAR)
        img_np = np.array(resized, dtype=np.float32) / 255.0

        # Normalize per channel: (x - mean) / std
        normalized = (img_np - cls.IMAGENET_MEAN) / cls.IMAGENET_STD

        # HWC -> CHW -> NCHW
        tensor = np.transpose(normalized, (2, 0, 1))
        tensor = np.expand_dims(tensor, axis=0)
        return tensor.astype(np.float32)

    @classmethod
    def check_leaf_likeness(cls, image: Image.Image) -> Tuple[bool, str]:
        """
        Simple biological sanity check analyzing color histograms
        to detect non-plant inputs (e.g. solid white screen, pets, vehicles).
        """
        img_np = np.array(image.resize((100, 100))) / 255.0
        r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

        # Calculate foliage/green-brown presence
        green_excess = (g - r) + (g - b)
        brown_presence = (r > 0.3) & (g > 0.2) & (b < 0.3)
        plant_pixels = (green_excess > 0.05) | brown_presence

        plant_ratio = np.mean(plant_pixels)
        if plant_ratio < 0.05:
            return False, "Image does not appear to contain plant foliage or leaves. Diagnosis confidence may be low."
        return True, ""
