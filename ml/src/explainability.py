"""
Grad-CAM heatmap generation for the trained MobileNetV2.
Produces per-image class activation maps saved as PNG overlays.

Usage:
  python -m ml.src.explainability --image path/to/leaf.jpg --class-idx 5
"""
import argparse
import numpy as np
from pathlib import Path
from PIL import Image

import torch
import torch.nn.functional as F

from ml.src.config import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


class GradCAM:
    """
    Gradient-weighted Class Activation Mapping (Grad-CAM).
    Works with any CNN that exposes a convolutional feature layer.
    """

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate(self, input_tensor: torch.Tensor, class_idx: int = None) -> np.ndarray:
        """
        Args:
            input_tensor: [1, 3, H, W] preprocessed tensor
            class_idx:    Target class (None = top predicted class)

        Returns:
            heatmap: [H, W] float32 array in [0, 1]
        """
        self.model.eval()
        input_tensor = input_tensor.requires_grad_(True)

        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = int(torch.argmax(output, dim=1).item())

        self.model.zero_grad()
        output[0, class_idx].backward()

        # Global average pool gradients over spatial dims
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)  # [1, C, 1, 1]
        cam = (weights * self.activations).sum(dim=1, keepdim=True)  # [1, 1, h, w]
        cam = F.relu(cam)

        # Normalize
        cam = cam.squeeze().cpu().numpy()
        if cam.max() > cam.min():
            cam = (cam - cam.min()) / (cam.max() - cam.min())
        else:
            cam = np.zeros_like(cam)

        return cam


def get_target_layer(model: torch.nn.Module, architecture: str = "mobilenet_v2"):
    """Returns the last convolutional feature layer for Grad-CAM."""
    if architecture == "mobilenet_v2":
        return model.features[-1]
    elif architecture == "efficientnet_b0":
        return model.features[-1]
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")


def overlay_heatmap(
    heatmap: np.ndarray,
    original_image: Image.Image,
    alpha: float = 0.4,
    colormap: str = "jet",
) -> Image.Image:
    """
    Overlays a Grad-CAM heatmap on the original leaf image.

    Args:
        heatmap:        [H, W] float array in [0, 1]
        original_image: PIL Image (RGB)
        alpha:          Heatmap opacity (0-1)

    Returns:
        PIL Image with Grad-CAM overlay
    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    # Resize heatmap to match original image
    h, w = original_image.size
    heatmap_resized = np.array(
        Image.fromarray((heatmap * 255).astype(np.uint8)).resize((h, w), Image.BILINEAR)
    ) / 255.0

    # Apply colormap
    cmap = cm.get_cmap(colormap)
    heatmap_rgb = (cmap(heatmap_resized)[:, :, :3] * 255).astype(np.uint8)
    heatmap_pil = Image.fromarray(heatmap_rgb).convert("RGBA")
    heatmap_pil.putalpha(int(alpha * 255))

    # Blend
    original_rgba = original_image.convert("RGBA")
    blended = Image.alpha_composite(original_rgba, heatmap_pil)
    return blended.convert("RGB")


def preprocess_image(image_path: str) -> tuple:
    """Loads and preprocesses a leaf image for inference."""
    import torchvision.transforms as T

    transform = T.Compose([
        T.Resize(int(IMAGE_SIZE * 1.14)),
        T.CenterCrop(IMAGE_SIZE),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)
    return tensor, img


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Grad-CAM for a leaf image")
    parser.add_argument("--image",     required=True,  help="Path to leaf image")
    parser.add_argument("--ckpt",      default=None,   help="Path to .pth checkpoint")
    parser.add_argument("--class-idx", type=int, default=None, help="Target class index")
    parser.add_argument("--output",    default="gradcam_output.png")
    args = parser.parse_args()

    import torchvision.models as models
    import torch.nn as nn
    from ml.src.config import NUM_CLASSES, CHECKPOINTS_DIR

    ckpt_dir = Path(CHECKPOINTS_DIR)
    ckpt_path = Path(args.ckpt) if args.ckpt else max(ckpt_dir.glob("*.pth"), key=lambda p: p.stat().st_mtime)

    ckpt = torch.load(ckpt_path, map_location="cpu")
    arch = ckpt.get("architecture", "mobilenet_v2")

    model = models.mobilenet_v2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(in_features, NUM_CLASSES))
    model.load_state_dict(ckpt["model_state_dict"])

    target_layer = get_target_layer(model, arch)
    grad_cam = GradCAM(model, target_layer)

    tensor, original = preprocess_image(args.image)
    heatmap = grad_cam.generate(tensor, class_idx=args.class_idx)
    result = overlay_heatmap(heatmap, original)
    result.save(args.output)
    print(f"[GradCAM] Saved overlay -> {args.output}")
