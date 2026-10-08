# Processed Dataset Directory

This directory stores preprocessed, split, and augmented dataset artifacts ready for model training and evaluation.

## Standard Layout
```
processed/
├── train/          # 70% of dataset
│   ├── Tomato___Early_blight/
│   └── ...
├── val/            # 15% of dataset (validation during training)
│   ├── Tomato___Early_blight/
│   └── ...
└── test/           # 15% of dataset (final unbiased evaluation)
    ├── Tomato___Early_blight/
    └── ...
```

## Image Specifications
- **Dimensions**: `224 x 224` pixels (RGB, 3 channels)
- **Normalization**: ImageNet standard (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`)
- **Format**: `.jpg` or `.png`
