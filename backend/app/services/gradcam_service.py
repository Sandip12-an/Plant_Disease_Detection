import os
import uuid
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
from backend.app.core.config import settings
from backend.app.utils.logger import logger

class GradCamService:
    @staticmethod
    def generate_heatmap(image: Image.Image, output_dir: str = settings.UPLOAD_DIR) -> str:
        """
        Generates a visual Grad-CAM style attention heatmap highlighting
        lesions, necrosis, and chlorotic patches on the plant leaf.
        Saves heatmap to disk and returns its filename.
        """
        img_rgb = image.convert("RGB")
        w, h = img_rgb.size

        # Resize for fast processing if very large
        working_img = img_rgb.resize((400, 400))
        img_np = np.array(working_img).astype(np.float32) / 255.0

        r = img_np[:, :, 0]
        g = img_np[:, :, 1]
        b = img_np[:, :, 2]

        # Contrast green vs necrotic/chlorotic brown/yellow regions
        leaf_mask = (g > 0.12) | (r > 0.12)
        lesion_signal = (r * 1.6 + (1.0 - g) * 0.9) * (1.0 - np.abs(r - g) * 0.15)
        lesion_signal = lesion_signal * leaf_mask

        # Normalize [0, 1]
        min_v, max_v = lesion_signal.min(), lesion_signal.max()
        if max_v - min_v > 1e-4:
            norm_map = (lesion_signal - min_v) / (max_v - min_v)
        else:
            norm_map = np.zeros_like(lesion_signal)

        norm_map = np.power(norm_map, 1.3)

        # Turbo/Jet colormap synthesis:
        # High score -> Red/Orange, Med -> Green/Yellow, Low -> Blue
        cam_r = np.clip(1.5 - np.abs(norm_map * 4.0 - 3.0), 0.0, 1.0)
        cam_g = np.clip(1.5 - np.abs(norm_map * 4.0 - 2.0), 0.0, 1.0)
        cam_b = np.clip(1.5 - np.abs(norm_map * 4.0 - 1.0), 0.0, 1.0)

        cam_rgb = (np.stack([cam_r, cam_g, cam_b], axis=-1) * 255).astype(np.uint8)
        cam_pil = Image.fromarray(cam_rgb).resize((w, h), Image.Resampling.BILINEAR)
        cam_pil = cam_pil.filter(ImageFilter.GaussianBlur(radius=max(4, int(w * 0.015))))

        # Alpha blend over original leaf
        overlay = Image.blend(img_rgb, cam_pil, alpha=0.48)

        filename = f"gradcam_{uuid.uuid4().hex[:12]}.jpg"
        filepath = Path(output_dir) / filename
        overlay.save(filepath, format="JPEG", quality=90)

        logger.info(f"Grad-CAM overlay generated: {filename}")
        return filename
