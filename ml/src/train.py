"""
Training loop for PlantVillage MobileNetV2.
Two-phase strategy:
  Phase 1 (epochs 1-5)  : Frozen backbone, train classifier only (high LR)
  Phase 2 (epochs 6+)   : Unfreeze backbone, fine-tune end-to-end (low LR)

Usage:
  python -m ml.src.train
  python -m ml.src.train --arch efficientnet_b0 --epochs 30 --batch 16
"""
import argparse
import json
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR

from ml.src.config import (
    DEVICE, NUM_EPOCHS, LEARNING_RATE, MIN_LEARNING_RATE,
    WEIGHT_DECAY, EARLY_STOPPING_PATIENCE, CHECKPOINTS_DIR, METRICS_PATH
)
from ml.src.dataset import build_dataloaders, set_seed
from ml.src.model import build_model, unfreeze_backbone
from ml.src.export import export_to_onnx


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def accuracy(outputs: torch.Tensor, labels: torch.Tensor) -> float:
    _, preds = torch.max(outputs, 1)
    return (preds == labels).float().mean().item()


def run_epoch(model, loader, criterion, optimizer, device, train=True):
    model.train(train)
    total_loss, total_acc, n = 0.0, 0.0, 0
    with torch.set_grad_enabled(train):
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            if train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            batch = len(labels)
            total_loss += loss.item() * batch
            total_acc  += accuracy(outputs, labels) * batch
            n += batch
    return total_loss / n, total_acc / n


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def train(
    architecture: str = "mobilenet_v2",
    num_epochs: int = NUM_EPOCHS,
    batch_size: int = 32,
    lr: float = LEARNING_RATE,
    weight_decay: float = WEIGHT_DECAY,
    unfreeze_epoch: int = 5,
    patience: int = EARLY_STOPPING_PATIENCE,
):
    set_seed()
    device = torch.device(DEVICE)
    print(f"[Train] Device: {device}  Architecture: {architecture}  Epochs: {num_epochs}")

    # Data
    train_loader, val_loader, _, class_to_idx, class_names = build_dataloaders(batch_size=batch_size)

    # Model
    model = build_model(architecture=architecture, pretrained=True).to(device)

    # Phase-1 optimizer (classifier only)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=lr, weight_decay=weight_decay
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=MIN_LEARNING_RATE)

    best_val_acc = 0.0
    patience_ctr = 0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    ckpt_dir = Path(CHECKPOINTS_DIR)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    best_ckpt = ckpt_dir / f"{architecture}_best.pth"

    for epoch in range(1, num_epochs + 1):
        t0 = time.time()

        # Phase-2: unfreeze backbone
        if epoch == unfreeze_epoch + 1:
            print(f"\n[Train] Epoch {epoch}: Unfreezing backbone for full fine-tuning...")
            model = unfreeze_backbone(model, architecture)
            optimizer = optim.AdamW(model.parameters(), lr=lr * 0.1, weight_decay=weight_decay)
            scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs - epoch, eta_min=MIN_LEARNING_RATE)

        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer, device, train=True)
        val_loss,   val_acc   = run_epoch(model, val_loader,   criterion, optimizer, device, train=False)
        scheduler.step()

        history["train_loss"].append(round(train_loss, 4))
        history["train_acc"].append(round(train_acc,   4))
        history["val_loss"].append(round(val_loss,     4))
        history["val_acc"].append(round(val_acc,       4))

        elapsed = time.time() - t0
        print(
            f"Epoch [{epoch:02d}/{num_epochs}]  "
            f"train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  "
            f"val_loss={val_loss:.4f}  val_acc={val_acc:.4f}  "
            f"lr={scheduler.get_last_lr()[0]:.2e}  time={elapsed:.1f}s"
        )

        # Checkpoint best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_ctr = 0
            torch.save({
                "epoch": epoch,
                "architecture": architecture,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_acc": val_acc,
                "class_to_idx": class_to_idx,
            }, best_ckpt)
            print(f"  -> New best val_acc={val_acc:.4f}, checkpoint saved.")
        else:
            patience_ctr += 1
            if patience_ctr >= patience:
                print(f"[Train] Early stopping triggered at epoch {epoch}.")
                break

    # Save training metrics
    metrics = {
        "architecture": architecture,
        "best_val_accuracy": round(best_val_acc, 4),
        "epochs_trained": epoch,
        "history": history,
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\n[Train] Metrics saved -> {METRICS_PATH}")
    print(f"[Train] Best val_acc = {best_val_acc:.4f}")

    # Load best weights and export to ONNX
    print("\n[Train] Loading best checkpoint for ONNX export...")
    ckpt = torch.load(best_ckpt, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    export_to_onnx(model, device=device)

    return model, history


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PlantVillage MobileNetV2")
    parser.add_argument("--arch",    default="mobilenet_v2", choices=["mobilenet_v2", "efficientnet_b0"])
    parser.add_argument("--epochs",  type=int,   default=NUM_EPOCHS)
    parser.add_argument("--batch",   type=int,   default=32)
    parser.add_argument("--lr",      type=float, default=LEARNING_RATE)
    parser.add_argument("--unfreeze-epoch", type=int, default=5)
    parser.add_argument("--patience", type=int,  default=EARLY_STOPPING_PATIENCE)
    args = parser.parse_args()

    train(
        architecture=args.arch,
        num_epochs=args.epochs,
        batch_size=args.batch,
        lr=args.lr,
        unfreeze_epoch=args.unfreeze_epoch,
        patience=args.patience,
    )
