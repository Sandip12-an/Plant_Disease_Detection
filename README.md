# Plant Disease Detection System 🌿🔬

An end-to-end deep learning and full-stack web platform for real-time agricultural crop disease diagnosis, visual explainability (Grad-CAM), and actionable biological & chemical treatment recommendations.

---

## 🌟 Key Features

- **Multi-Crop Coverage**: Recognizes 38 disease and healthy classes across 14 crop species (Tomato, Potato, Corn, Apple, Grape, Peach, Bell Pepper, Strawberry, etc.).
- **High-Speed Inference**: Powered by an optimized **MobileNetV2 ONNX Runtime** pipeline delivering sub-30ms predictions.
- **Visual Explainability (Grad-CAM)**: Generates class activation heatmaps so farmers and agronomists can visually verify which lesions the model detected on the leaf.
- **Actionable Remedy Plans**: Comprehensive treatment recommendations categorized into:
  - 🌿 **Organic / Biological Controls** (Neem oil, Bacillus subtilis, bio-fungicides)
  - 🧪 **Chemical Treatments** (Active ingredients, targeted fungicides, spray intervals)
  - 🛡️ **Cultural & Preventive Measures** (Crop rotation, watering hygiene, spacing)
- **Modern Full-Stack Experience**:
  - **FastAPI** backend with automated OpenAPI/Swagger documentation, SQLite/PostgreSQL support, and JWT authentication.
  - **React + Vite** frontend featuring live camera capture, drag-and-drop uploads, interactive Grad-CAM comparison slider, disease encyclopedia, and scan history.
- **Containerized & CI Ready**: Complete Docker Compose setups and automated GitHub Actions workflows.

---

## 📂 Repository Structure

```
Plant_disease_detection/
├── .github/
│   └── workflows/
│       ├── ci-backend.yml              # Backend unit tests and linting
│       ├── ci-frontend.yml             # Frontend build and tests
│       └── model-pipeline.yml          # Automated model evaluation/validation
│
├── data/                               # Local dataset storage (gitignored)
│   ├── raw/                            # Raw PlantVillage / PlantDoc datasets
│   ├── processed/                      # Resized, normalized, split (train/val/test)
│   └── sample_images/                  # Test sample images for API and manual verification
│
├── ml/                                 # Machine Learning & Model Development
│   ├── notebooks/                      # Jupyter notebooks for EDA & prototyping
│   │   ├── 01_exploratory_data_analysis.ipynb
│   │   ├── 02_baseline_cnn.ipynb
│   │   └── 03_transfer_learning_experiments.ipynb
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config.py                   # Hyperparameters, paths, and image specs (224x224)
│   │   ├── dataset.py                  # PyTorch DataLoader & augmentations
│   │   ├── model.py                    # Model architectures (MobileNetV2, EfficientNet-B0)
│   │   ├── train.py                    # Training & validation loop with early stopping
│   │   ├── evaluate.py                 # Precision, Recall, F1, and Confusion Matrix
│   │   ├── export.py                   # Model conversion to ONNX and TFLite
│   │   └── explainability.py           # Grad-CAM heatmap generation for affected leaf areas
│   ├── model_registry/                 # Exported model weights & metadata
│   │   ├── mobilenet_v2_v1.onnx
│   │   ├── mobilenet_v2_v1.tflite
│   │   ├── class_labels.json           # 38 PlantVillage disease class mappings
│   │   └── metrics.json                # Validation metrics record
│   └── requirements-ml.txt             # ML-specific dependencies
│
├── backend/                            # FastAPI REST API & Inference Engine
│   ├── app/
│   │   ├── main.py                     # FastAPI application entrypoint & middleware setup
│   │   ├── core/                       # App settings, DB session, JWT security
│   │   ├── api/v1/endpoints/           # /predict, /history, /diseases, /auth, /health
│   │   ├── models/                     # SQLAlchemy models (User, Scan, Disease)
│   │   ├── schemas/                    # Pydantic schemas (Request/Response)
│   │   ├── services/                   # Inference, Image Preprocessing, Grad-CAM, Storage
│   │   ├── db/seed_data/               # 38-class agronomic disease & remedy database
│   │   └── utils/                      # Structured logging & custom exception handlers
│   ├── tests/                          # Backend pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                           # Client Application (React + Vite)
│   ├── src/
│   │   ├── components/                 # Camera, DropZone, Diagnosis, Grad-CAM, Treatments
│   │   ├── pages/                      # Home, Scan, History, Disease Directory, Disease Detail
│   │   ├── services/                   # Axios API clients
│   │   ├── styles/index.css            # Bespoke botanical emerald design system
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml                  # Local development orchestration
├── docker-compose.prod.yml             # Production deployment orchestration
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- Docker (optional, for containerized run)

### 1. Run Backend Locally

```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/api/v1/health`

### 2. Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

### 3. Run with Docker Compose

```bash
docker-compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/predict` | Uploads leaf photo, returns disease class, confidence, Grad-CAM, and remedy |
| `GET` | `/api/v1/diseases` | Lists all 38 diseases with filters for crop type |
| `GET` | `/api/v1/diseases/{id}` | Detailed symptoms, causes, and organic & chemical treatments |
| `GET` | `/api/v1/history` | Fetches user's previous scan history |
| `POST` | `/api/v1/auth/register` | Registers a new user account |
| `POST` | `/api/v1/auth/login` | Authenticates user and returns JWT token |
| `GET` | `/api/v1/health` | Service liveness and model engine readiness check |

---

## 🔬 Model Architecture & Training

The classification system is based on **MobileNetV2** and **EfficientNet-B0** backbones pre-trained on ImageNet and fine-tuned on the PlantVillage and PlantDoc datasets:
1. Input size: `224x224x3`.
2. Color and spatial augmentations: Random rotation, perspective jitter, brightness/contrast shifts, and simulated outdoor lighting variations.
3. Exported to **ONNX** format for cross-platform, low-latency deployment.
