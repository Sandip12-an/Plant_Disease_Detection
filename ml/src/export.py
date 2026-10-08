"""
ONNX (and optional TFLite) export for the trained PlantVillage model.

Usage:
  python -m ml.src.export                        # exports from best checkpoint
  python -m ml.src.export --ckpt <path.pth>
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from ml.src.config import (
    ONNX_EXPORT_PATH, TFLITE_EXPORT_PATH, CHECKPOINTS_DIR,
    IMAGE_SIZE, NUM_CLASSES, MODEL_REGISTRY_DIR
)


def export_to_onnx(
    model: nn.Module,
    export_path: Path = None,
    image_size: int = IMAGE_SIZE,
    device: torch.device = None,
) -> Path:
    """
    Exports a PyTorch model to ONNX format with dynamic batch axis.

    Args:
        model:       Trained nn.Module
        export_path: Destination .onnx file (defaults to config path)
        image_size:  Input spatial dimension (224)
        device:      torch.device

    Returns:
        Path to the exported .onnx file
    """
    if export_path is None:
        export_path = Path(ONNX_EXPORT_PATH)
    export_path = Path(export_path)
    export_path.parent.mkdir(parents=True, exist_ok=True)

    if device is None:
        device = torch.device("cpu")

    model.eval().to(device)
    dummy_input = torch.randn(1, 3, image_size, image_size, device=device)

    torch.onnx.export(
        model,
        dummy_input,
        str(export_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input":  {0: "batch_size"},
            "output": {0: "batch_size"},
        },
    )

    size_mb = export_path.stat().st_size / (1024 * 1024)
    print(f"[Export] ONNX model saved -> {export_path}  ({size_mb:.2f} MB)")
    return export_path


def verify_onnx(export_path: Path = None):
    """Runs a quick ONNX Runtime sanity-check on the exported model."""
    import onnxruntime as ort

    if export_path is None:
        export_path = Path(ONNX_EXPORT_PATH)

    session = ort.InferenceSession(str(export_path), providers=["CPUExecutionProvider"])
    dummy = np.random.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE).astype(np.float32)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: dummy})
    logits = outputs[0][0]
    probs = np.exp(logits - logits.max()) / np.exp(logits - logits.max()).sum()

    top_idx = int(np.argmax(probs))
    top_prob = float(probs[top_idx])
    print(f"[Export] ONNX verify OK  output_shape={outputs[0].shape}  top_class={top_idx}  confidence={top_prob:.4f}")


def generate_synthetic_onnx_model(export_path: str):
    """
    Fallback: generates a real (randomly-initialized) MobileNetV2 ONNX model.
    This still produces uniform predictions but is structurally correct.
    Only used when no trained checkpoint exists.
    """
    import torchvision.models as models

    print("[Export] Generating synthetic MobileNetV2 ONNX (no trained weights)...")
    model = models.mobilenet_v2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(in_features, NUM_CLASSES),
    )
    export_to_onnx(model, export_path=Path(export_path))
    print("[Export] Synthetic model ready. Train a real model for useful predictions.")


def export_from_checkpoint(ckpt_path: Path = None):
    """Loads the best checkpoint and re-exports to ONNX."""
    import torchvision.models as models

    if ckpt_path is None:
        # Auto-find most recent checkpoint
        ckpt_dir = Path(CHECKPOINTS_DIR)
        candidates = list(ckpt_dir.glob("*.pth"))
        if not candidates:
            raise FileNotFoundError(f"No .pth checkpoints found in {ckpt_dir}")
        ckpt_path = max(candidates, key=lambda p: p.stat().st_mtime)

    print(f"[Export] Loading checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location="cpu")
    arch = ckpt.get("architecture", "mobilenet_v2")

    if arch == "mobilenet_v2":
        model = models.mobilenet_v2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features, NUM_CLASSES),
        )
    elif arch == "efficientnet_b0":
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features, NUM_CLASSES),
        )
    else:
        raise ValueError(f"Unknown architecture in checkpoint: {arch}")

    model.load_state_dict(ckpt["model_state_dict"])
    path = export_to_onnx(model)
    verify_onnx(path)
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export PlantVillage model to ONNX")
    parser.add_argument("--ckpt", type=str, default=None, help="Path to .pth checkpoint")
    parser.add_argument("--verify", action="store_true", help="Verify exported ONNX model")
    args = parser.parse_args()

    ckpt_path = Path(args.ckpt) if args.ckpt else None
    out = export_from_checkpoint(ckpt_path)

    if args.verify:
        verify_onnx(out)
