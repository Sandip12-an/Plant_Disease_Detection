import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TRAIN_DATA_DIR = PROCESSED_DATA_DIR / "train"
VAL_DATA_DIR = PROCESSED_DATA_DIR / "val"
TEST_DATA_DIR = PROCESSED_DATA_DIR / "test"

MODEL_REGISTRY_DIR = BASE_DIR / "ml" / "model_registry"
CHECKPOINTS_DIR = BASE_DIR / "ml" / "checkpoints"
METRICS_PATH = MODEL_REGISTRY_DIR / "metrics.json"
CLASS_LABELS_PATH = MODEL_REGISTRY_DIR / "class_labels.json"
ONNX_EXPORT_PATH = MODEL_REGISTRY_DIR / "mobilenet_v2_v1.onnx"
TFLITE_EXPORT_PATH = MODEL_REGISTRY_DIR / "mobilenet_v2_v1.tflite"

# Ensure registry & checkpoint directories exist
os.makedirs(MODEL_REGISTRY_DIR, exist_ok=True)
os.makedirs(CHECKPOINTS_DIR, exist_ok=True)

# Image & Preprocessing Specifications
IMAGE_SIZE = 224
CHANNELS = 3
NUM_CLASSES = 38
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Training Hyperparameters
BATCH_SIZE = 32
NUM_EPOCHS = 25
LEARNING_RATE = 1e-4
MIN_LEARNING_RATE = 1e-6
WEIGHT_DECAY = 1e-4
DROPOUT_RATE = 0.3
EARLY_STOPPING_PATIENCE = 5
NUM_WORKERS = 4
SEED = 42

# Device Configuration
import torch as _torch
DEVICE = "cuda" if _torch.cuda.is_available() else "cpu"
del _torch
