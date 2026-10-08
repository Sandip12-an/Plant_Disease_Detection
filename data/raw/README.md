# Raw Dataset Directory

This directory stores the original, unprocessed datasets used for training the Plant Disease Detection models.

## Expected Datasets

1. **PlantVillage Dataset**:
   - Contains ~54,306 images across 38 crop disease and healthy classes.
   - Recommended source: [PlantVillage on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease) or [Torchvision Datasets](https://pytorch.org/vision/main/generated/torchvision.datasets.PlantVillage.html).
   - Format: Folder structure organized by class:
     ```
     raw/
     ├── Apple___Apple_scab/
     ├── Apple___Black_rot/
     ├── Apple___Cedar_apple_rust/
     ├── Apple___healthy/
     ├── Tomato___Bacterial_spot/
     ├── Tomato___Early_blight/
     ├── Tomato___Late_blight/
     └── ...
     ```

2. **PlantDoc Dataset (Field Images)**:
   - Contains ~2,598 real-field images with challenging natural backgrounds and outdoor lighting.
   - Used to boost real-world field robustness and reduce the lab domain shift.

> **Note**: Raw dataset files are excluded from git via `.gitignore`.
