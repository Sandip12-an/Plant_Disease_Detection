"""
Model evaluation: Accuracy, Precision, Recall, F1, Confusion Matrix.

Usage:
  python -m ml.src.evaluate                     # evaluates best checkpoint on test set
  python -m ml.src.evaluate --ckpt <path.pth>
  python -m ml.src.evaluate --onnx              # evaluate the exported ONNX model
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score
)

from ml.src.config import (
    DEVICE, CHECKPOINTS_DIR, METRICS_PATH, ONNX_EXPORT_PATH,
    CLASS_LABELS_PATH, IMAGE_SIZE
)
from ml.src.dataset import build_dataloaders


# ---------------------------------------------------------------------------
# PyTorch evaluation
# ---------------------------------------------------------------------------

def evaluate_pytorch(ckpt_path: Path = None):
    import torchvision.models as models
    import torch.nn as nn

    from ml.src.config import NUM_CLASSES

    if ckpt_path is None:
        ckpt_dir = Path(CHECKPOINTS_DIR)
        candidates = list(ckpt_dir.glob("*.pth"))
        if not candidates:
            raise FileNotFoundError(f"No checkpoints in {ckpt_dir}")
        ckpt_path = max(candidates, key=lambda p: p.stat().st_mtime)

    print(f"[Evaluate] Loading checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location="cpu")
    arch = ckpt.get("architecture", "mobilenet_v2")

    if arch == "mobilenet_v2":
        model = models.mobilenet_v2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(in_features, NUM_CLASSES))
    else:
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(in_features, NUM_CLASSES))

    model.load_state_dict(ckpt["model_state_dict"])
    device = torch.device(DEVICE)
    model.eval().to(device)

    _, _, test_loader, class_to_idx, class_names = build_dataloaders()

    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images.to(device))
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    return _report(all_labels, all_preds, class_names, tag="PyTorch")


# ---------------------------------------------------------------------------
# ONNX evaluation
# ---------------------------------------------------------------------------

def evaluate_onnx():
    import onnxruntime as ort

    session = ort.InferenceSession(str(ONNX_EXPORT_PATH), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    _, _, test_loader, _, class_names = build_dataloaders()

    all_preds, all_labels = [], []
    for images, labels in test_loader:
        imgs_np = images.numpy().astype(np.float32)
        outputs = session.run(None, {input_name: imgs_np})
        preds = np.argmax(outputs[0], axis=1)
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.numpy().tolist())

    return _report(all_labels, all_preds, class_names, tag="ONNX")


# ---------------------------------------------------------------------------
# Shared reporting
# ---------------------------------------------------------------------------

def _report(y_true, y_pred, class_names, tag="Model"):
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec  = recall_score(y_true, y_pred,    average="weighted", zero_division=0)
    f1   = f1_score(y_true, y_pred,        average="weighted", zero_division=0)

    print(f"\n[Evaluate] {tag} Results")
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-Score  : {f1:.4f}")
    print("\nPer-class Report:")
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

    metrics = {
        "tag": tag,
        "test_accuracy":  round(acc,  4),
        "test_precision": round(prec, 4),
        "test_recall":    round(rec,  4),
        "test_f1":        round(f1,   4),
    }

    # Merge with existing metrics file
    existing = {}
    if Path(METRICS_PATH).exists():
        with open(METRICS_PATH) as f:
            existing = json.load(f)
    existing.update(metrics)
    with open(METRICS_PATH, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"[Evaluate] Metrics saved -> {METRICS_PATH}")
    return metrics


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, default=None)
    parser.add_argument("--onnx", action="store_true", help="Evaluate ONNX model instead of PyTorch")
    args = parser.parse_args()

    if args.onnx:
        evaluate_onnx()
    else:
        evaluate_pytorch(Path(args.ckpt) if args.ckpt else None)
