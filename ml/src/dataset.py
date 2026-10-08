"""
PlantVillage Dataset loader with train/val/test splits and augmentations.
Expects data in: data/processed/{train,val,test}/<ClassName>/image.jpg
"""
import os
import json
import random
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Tuple, List, Optional

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T

from ml.src.config import (
    TRAIN_DATA_DIR, VAL_DATA_DIR, TEST_DATA_DIR,
    CLASS_LABELS_PATH, IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD,
    BATCH_SIZE, NUM_WORKERS, SEED, NUM_CLASSES
)


def set_seed(seed: int = SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------

def get_train_transforms() -> T.Compose:
    return T.Compose([
        T.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.RandomRotation(30),
        T.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),
        T.RandomPerspective(distortion_scale=0.2, p=0.3),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_val_transforms() -> T.Compose:
    return T.Compose([
        T.Resize(int(IMAGE_SIZE * 1.14)),
        T.CenterCrop(IMAGE_SIZE),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class PlantDiseaseDataset(Dataset):
    """
    Folder-based image classification dataset.
    Each sub-folder name is treated as a class label.
    """

    def __init__(
        self,
        root_dir: Path,
        transform=None,
        class_to_idx=None,
    ):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.samples: List[Tuple[Path, int]] = []

        if not self.root_dir.exists():
            raise FileNotFoundError(
                f"Dataset directory not found: {self.root_dir}\n"
                "Download PlantVillage and place in data/processed/{train,val,test}/"
            )

        classes = sorted([
            d.name for d in self.root_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ])
        if not classes:
            raise RuntimeError(f"No class sub-folders found in {self.root_dir}")

        if class_to_idx is None:
            self.class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
        else:
            self.class_to_idx = class_to_idx

        self.classes = list(self.class_to_idx.keys())

        VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        for cls_name, idx in self.class_to_idx.items():
            cls_dir = self.root_dir / cls_name
            if not cls_dir.exists():
                continue
            for img_path in cls_dir.iterdir():
                if img_path.suffix.lower() in VALID_EXTS:
                    self.samples.append((img_path, idx))

        if not self.samples:
            raise RuntimeError(f"No images found under {self.root_dir}.")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        img_path, label = self.samples[index]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label


# ---------------------------------------------------------------------------
# DataLoader factory
# ---------------------------------------------------------------------------

def build_dataloaders(batch_size=BATCH_SIZE, num_workers=NUM_WORKERS, pin_memory=True):
    """Returns (train_loader, val_loader, test_loader, class_to_idx, class_names)."""
    set_seed()

    train_ds = PlantDiseaseDataset(TRAIN_DATA_DIR, transform=get_train_transforms())
    class_to_idx = train_ds.class_to_idx
    class_names = train_ds.classes

    val_ds  = PlantDiseaseDataset(VAL_DATA_DIR,  transform=get_val_transforms(), class_to_idx=class_to_idx)
    test_ds = PlantDiseaseDataset(TEST_DATA_DIR, transform=get_val_transforms(), class_to_idx=class_to_idx)

    idx_to_class = {v: k for k, v in class_to_idx.items()}
    class_labels_list = [idx_to_class[i] for i in range(len(idx_to_class))]
    with open(CLASS_LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(class_labels_list, f, indent=2)
    print(f"[Dataset] Saved {len(class_labels_list)} class labels -> {CLASS_LABELS_PATH}")

    _kw = dict(batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory)
    train_loader = DataLoader(train_ds, shuffle=True,  **_kw)
    val_loader   = DataLoader(val_ds,   shuffle=False, **_kw)
    test_loader  = DataLoader(test_ds,  shuffle=False, **_kw)

    print(f"[Dataset] train={len(train_ds):,}  val={len(val_ds):,}  test={len(test_ds):,}  classes={len(class_names)}")
    return train_loader, val_loader, test_loader, class_to_idx, class_names
