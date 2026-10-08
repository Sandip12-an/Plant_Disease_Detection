# Plant Disease Detection — Implementation Plan

## 1. Project Overview

**Goal:** Build a system that takes an image of a plant leaf and classifies it as healthy or diseased, identifying the specific disease and optionally severity/treatment recommendations.

**Core use case:** Farmer/user uploads or captures a leaf photo → system predicts disease → returns diagnosis + confidence + remedy suggestion.

---

## 2. Requirements

### Functional
- Accept image input (upload/camera)
- Preprocess image (resize, normalize, augment)
- Classify disease using a trained model
- Return prediction + confidence score
- Show remedy/treatment info
- Store history of past scans (optional)
- Support multiple crops (tomato, potato, corn, etc.)

### Non-Functional
- Inference latency < 2–3 sec
- Mobile-friendly (works on low bandwidth)
- Scalable to handle concurrent users
- Model accuracy > 90% on validation set
- Offline capability (optional, via on-device model)

---

## 3. Dataset

- **PlantVillage dataset** (most common starting point — ~54,000 images, 38 classes across 14 crops)
- Optionally supplement with **PlantDoc** (real-world field images, less clean but more realistic)
- Split: 70% train / 15% validation / 15% test
- Consider class imbalance — some diseases have far fewer images

---

## 4. Model Design

### Approach options
| Approach | Pros | Cons |
|---|---|---|
| Custom CNN from scratch | Full control, lightweight | Needs more data/tuning |
| Transfer Learning (ResNet50, MobileNetV2, EfficientNet) | Faster training, higher accuracy, less data needed | Larger model size (except MobileNet) |
| Vision Transformer (ViT) | State-of-art accuracy | Needs more compute/data |

**Recommended:** Transfer learning with **MobileNetV2** or **EfficientNet-B0** — good accuracy/speed tradeoff, deployable on mobile/edge.

### Training pipeline
1. Load & augment data (rotation, flip, zoom, brightness shift — leaves vary a lot in field conditions)
2. Load pretrained backbone (ImageNet weights), freeze base layers initially
3. Add custom classification head (GAP → Dense → Dropout → Softmax)
4. Train head first, then fine-tune top layers with low learning rate
5. Evaluate: accuracy, precision/recall/F1 per class, confusion matrix
6. Export model (ONNX/TFLite for mobile deployment)

---

## 5. Implementation Plan (Phased)

### Phase 1 — Data & Baseline (Week 1–2)
- Collect/download dataset, explore class distribution
- Build preprocessing & augmentation pipeline
- Train a baseline CNN, get initial accuracy numbers

### Phase 2 — Model Development (Week 3–4)
- Implement transfer learning model
- Hyperparameter tuning (learning rate, batch size, augmentation strength)
- Evaluate on validation/test sets, analyze misclassifications

### Phase 3 — Backend & API (Week 5)
- Build FastAPI service with `/predict` endpoint
- Integrate model inference (batch + single image)
- Add image validation, error handling

### Phase 4 — Frontend (Week 6)
- Build upload/camera UI
- Display prediction, confidence, disease info, treatment suggestions
- Handle loading/error states

### Phase 5 — Database & History (Week 7)
- Store scan history per user
- Build disease-info knowledge base (symptoms, treatment, prevention)

### Phase 6 — Deployment (Week 8)
- Containerize with Docker
- Deploy backend (AWS/GCP/Render/Railway)
- Convert model to TFLite for mobile app, or deploy as cloud API
- Set up CI/CD, monitoring, logging

### Phase 7 — Testing & Iteration
- Field-test with real (not just PlantVillage-clean) images
- Collect feedback, retrain with harder/misclassified examples
- Add active learning loop for continuous improvement

---

## 6. Tech Stack Suggestion

| Layer | Tools |
|---|---|
| Model training | PyTorch / TensorFlow-Keras |
| Model serving | TorchServe / TensorFlow Serving / ONNX Runtime |
| Backend API | FastAPI |
| Frontend | React (web) or Flutter (mobile) |
| Database | PostgreSQL (structured) or MongoDB (flexible) |
| Storage | AWS S3 / local filesystem |
| Deployment | Docker + AWS EC2/GCP Cloud Run / Render |
| Monitoring | Prometheus + Grafana, or simple logging + Sentry |

---

## 7. Extra Features (Stretch Goals)
- Severity estimation (mild/moderate/severe) via segmentation
- Multi-leaf detection in one image (object detection with YOLO)
- Explainability (Grad-CAM heatmaps showing infected regions)
- Offline mobile inference (TFLite model on-device)
- Multilingual treatment advice for farmers
- Chatbot integration for follow-up Q&A on treatment
